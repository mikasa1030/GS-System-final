from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, TaskViewSet, AnnotationViewSet

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet, basename='dataset')
router.register(r'tasks', TaskViewSet)
router.register(r'annotations', AnnotationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
