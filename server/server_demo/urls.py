from django.contrib import admin
from django.urls import path, include
from api.views import upload_file, upload_head, list_uploaded_files, segment_image

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('upload/', upload_file),
    path('uploadhead/', upload_head),
    path('list_uploaded_files/', list_uploaded_files),
    path('segment/', segment_image),
]
