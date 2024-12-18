from rest_framework import permissions
from project.models import Project
from .models import Task


class IsProjectMember(permissions.BasePermission):
    def has_permission(self, request, view):
        project_id = view.kwargs.get("project_id")

        if not project_id:
            task_id = view.kwargs.get("id")
            if not task_id:
                return False
            try:
                project_id = Task.objects.get(pk=task_id).project_id
            except Task.DoesNotExist:
                return False 
        return Project.objects.filter(id=project_id, members__user=request.user).exists()

