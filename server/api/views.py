import os
import datetime
from django.conf import settings
from rest_framework import viewsets, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task, Annotation
from .serializers import TaskSerializer, AnnotationSerializer

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
