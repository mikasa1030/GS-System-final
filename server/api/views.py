import os
import datetime
from django.conf import settings
from rest_framework import viewsets, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task, Annotation
from .serializers import TaskSerializer, AnnotationSerializer
from .sam_service import SAMService
import json

class DatasetViewSet(viewsets.ViewSet):
    """
    View to list datasets and their contents from the filesystem.
    """
    def list(self, request):
        root = settings.DATASETS_ROOT
        if not os.path.exists(root):
            return Response([], status=status.HTTP_200_OK)
        
        datasets = []
        try:
            for i, name in enumerate(os.listdir(root)):
                path = os.path.join(root, name)
                if os.path.isdir(path):
                    # Count scenes
                    scenes = []
                    try:
                        scenes = [s for s in os.listdir(path) if os.path.isdir(os.path.join(path, s))]
                    except OSError:
                        pass
                        
                    # Get modification time
                    mtime = os.path.getmtime(path)
                    date_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')

                    datasets.append({
                        'id': i + 1,
                        'name': name,
                        'path': path,
                        'sceneCount': len(scenes),
                        'scenes': scenes,
                        'date': date_str,
                        'expanded': False # Frontend helper
                    })
        except OSError as e:
            return Response({'error': str(e)}, status=500)
            
        return Response(datasets)

    @action(detail=False, methods=['get'])
    def images(self, request):
        dataset = request.query_params.get('dataset')
        scene = request.query_params.get('scene')
        
        if not dataset or not scene:
            return Response({'error': 'Missing dataset or scene parameter'}, status=400)
            
        root = settings.DATASETS_ROOT
        
        # Define potential image directories to scan
        subdirs = ['images', 'weather_images']
        images = []
        
        for subdir in subdirs:
            images_path = os.path.join(root, dataset, scene, subdir)
            if os.path.exists(images_path):
                try:
                    for name in os.listdir(images_path):
                        if name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                            # Use /@fs/ prefix for Vite
                            url = f"/@fs/{images_path}/{name}".replace("\\", "/")
                            # Add subdir prefix to name to distinguish
                            display_name = f"{subdir}/{name}" if len(subdirs) > 1 else name
                            images.append({'name': display_name, 'url': url})
                except OSError:
                    pass
        
        if not images:
            return Response([], status=200)
        
        # Sort images by name
        images.sort(key=lambda x: x['name'])
        
        return Response(images)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.status = 'completed'
        task.save()
        return Response({'status': 'completed'})

class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer

# Custom views for file upload support
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        folder = request.POST.get('folder', 'uploads') # Try to get folder from form data
        
        if not file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
            
        root = getattr(settings, 'DATASETS_ROOT', 'D:/datasets')
        save_dir = os.path.join(root, folder)
        os.makedirs(save_dir, exist_ok=True)
        
        save_path = os.path.join(save_dir, file.name)
        
        try:
            with open(save_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            return JsonResponse({'status': 'success', 'filename': file.name, 'path': save_path})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def upload_head(request):
    # Logic for head upload, reuse upload_file for now but maybe different folder
    if request.method == 'POST':
        # Inject folder 'head' if not present
        request.POST._mutable = True
        request.POST['folder'] = 'head'
        request.POST._mutable = False
        return upload_file(request)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def segment_image(request):
    """
    API endpoint for SAM segmentation
    Expected JSON body:
    {
        "image_url": "/@fs/D:/datasets/...",
        "points": [{"x": 0.5, "y": 0.5}], 
        "box": {"x": 0.1, "y": 0.1, "w": 0.5, "h": 0.5},
        "width": 1920,
        "height": 1080
    }
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"Segment request data: {data}") # Debug print
            
            # Extract image path from URL
            # URL format: /@fs/D:/datasets/... -> D:/datasets/...
            image_url = data.get('image_url')
            
            if not image_url:
                print("Error: No image_url provided")
                return JsonResponse({'error': 'No image_url provided'}, status=400)

            image_path = ""
            if '/@fs/' in image_url:
                image_path = image_url.split('/@fs/')[1]
            else:
                # Handle cases without /@fs/ (e.g., demo images in public folder)
                # Try to locate it in the web/public directory relative to project root if possible
                # Assuming standard layout: root/server and root/web
                # D:/GS-System/server/api/views.py -> D:/GS-System/web/public
                current_dir = os.path.dirname(os.path.abspath(__file__)) # server/api
                project_root = os.path.dirname(os.path.dirname(current_dir)) # D:/GS-System
                
                # Remove leading slash if present
                clean_url = image_url.lstrip('/')
                potential_path = os.path.join(project_root, 'web', 'public', clean_url)
                
                if os.path.exists(potential_path):
                    image_path = potential_path
                else:
                    print(f"Error: Invalid image URL format and file not found: {image_url}")
                    return JsonResponse({'error': f'Invalid image URL: {image_url}'}, status=400)
            
            # URL decode the path just in case
            import urllib.parse
            image_path = urllib.parse.unquote(image_path)
            
            print(f"Processing image path: {image_path}")
            
            if not os.path.exists(image_path):
                 print(f"Error: Image file does not exist at {image_path}")
                 return JsonResponse({'error': f'Image file not found at {image_path}'}, status=404)

            # Parse inputs
            
            # Parse inputs
            width = data.get('width')
            height = data.get('height')
            points = data.get('points', [])
            box = data.get('box')
            
            sam_points = []
            sam_labels = []
            sam_box = None
            
            # Convert relative coordinates to absolute pixel coordinates
            if points:
                for p in points:
                    sam_points.append([p['x'] * width, p['y'] * height])
                    sam_labels.append(1) # Default to foreground
            
            if box:
                # box format from frontend: x, y, w, h (relative)
                # SAM expects: x1, y1, x2, y2 (absolute)
                x1 = box['x'] * width
                y1 = box['y'] * height
                x2 = (box['x'] + box['w']) * width
                y2 = (box['y'] + box['h']) * height
                sam_box = [x1, y1, x2, y2]
                
            # Get SAM service
            sam_service = SAMService.get_instance()
            result = sam_service.predict(
                image_path=image_path,
                points=sam_points if sam_points else None,
                labels=sam_labels if sam_labels else None,
                box=sam_box
            )
            
            return JsonResponse(result)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def list_uploaded_files(request):
    folder_key = request.GET.get('folder_key', 'uploads')
    root = getattr(settings, 'DATASETS_ROOT', 'D:/datasets')
    target_dir = os.path.join(root, folder_key if folder_key != 'default' else 'uploads')
    
    files = []
    if os.path.exists(target_dir):
        try:
            for name in os.listdir(target_dir):
                path = os.path.join(target_dir, name)
                if os.path.isfile(path):
                    files.append({
                        'name': name,
                        'url': f'/@fs/{path}'.replace('\\', '/'), # Vite friendly url
                        'size': os.path.getsize(path)
                    })
        except OSError:
            pass
            
    return JsonResponse(files, safe=False)
