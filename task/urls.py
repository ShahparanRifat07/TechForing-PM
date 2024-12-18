from django.urls import path
from .views import TaskListAPIView, TaskDetailAPIView

urlpatterns = [
    path('api/projects/<int:project_id>/tasks/', TaskListAPIView.as_view(), name='task-list-create'),
    path('api/tasks/<int:id>/', TaskDetailAPIView.as_view(), name='task-detail'),
]