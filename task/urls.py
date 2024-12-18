from django.urls import path
from .views import TaskListAPIView, TaskDetailAPIView, CommentListAPIView, CommentDetailAPIView

urlpatterns = [
    path('api/projects/<int:project_id>/tasks/', TaskListAPIView.as_view(), name='task-list-create'),
    path('api/tasks/<int:id>/', TaskDetailAPIView.as_view(), name='task-detail'),
    path('api/tasks/<int:task_id>/comments/', CommentListAPIView.as_view(), name='comment-list-create'),
    path('api/comments/<int:id>/', CommentDetailAPIView.as_view(), name='comment-detail'),
    
]

