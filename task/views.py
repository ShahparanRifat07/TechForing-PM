from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import get_object_or_404

from .models import Task, Comment, Project
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
)
from .permissions import IsProjectMember, IsCommentOwner


class TaskListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProjectMember]

    @swagger_auto_schema(
        tags=["tasks"],
    )
    def get(self, request, project_id):
        try:
            tasks = Task.objects.filter(project_id=project_id)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=["tasks"],
        request_body=TaskCreateSerializer,
    )
    def post(self, request, project_id):
        try:
            project = get_object_or_404(Project, pk=project_id)
            serializer = TaskCreateSerializer(
                data=request.data, context={"request": request, "project": project}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProjectMember]

    @swagger_auto_schema(
        tags=["tasks"],
    )
    def get_object(self, id):
        return get_object_or_404(Task, pk=id)

    @swagger_auto_schema(
        tags=["tasks"],
    )
    def get(self, request, id):
        try:
            task = self.get_object(id)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=["tasks"],
        request_body=TaskCreateSerializer,
    )
    def put(self, request, id):
        try:
            task = self.get_object(id)
            serializer = TaskCreateSerializer(
                task, data=request.data, context={"request": request, "task": task}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=["tasks"],
        request_body=TaskCreateSerializer,
    )
    def patch(self, request, id):
        try:
            task = self.get_object(id)
            serializer = TaskCreateSerializer(
                task,
                data=request.data,
                partial=True,
                context={"request": request, "task": task},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=["tasks"])
    def delete(self, request, id):
        try:
            task = self.get_object(id)
            task.delete()
            return Response(
                {"detail": "Task deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CommentListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCommentOwner]

    @swagger_auto_schema(
        tags=["comments"],
    )
    def get(self, request, task_id):
        try:
            comment = Comment.objects.filter(task_id=task_id)
            serializer = CommentSerializer(comment, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=["comments"],
        request_body=CommentCreateSerializer,
    )
    def post(self, request, task_id):
        try:
            task = get_object_or_404(Task, id=task_id)
            serializer = CommentCreateSerializer(
                data=request.data, context={"request": request, "task": task}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCommentOwner]

    @swagger_auto_schema(
        tags=["comments"],
    )
    def get_object(self, id):
        return get_object_or_404(Comment, pk=id)

    @swagger_auto_schema(
        tags=["comments"],
    )
    def get(self, request, id):
        try:
            comment = self.get_object(id)
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=["comments"],
        request_body=CommentCreateSerializer,
    )
    def put(self, request, id):
        try:
            comment = self.get_object(id)
            serializer = CommentCreateSerializer(
                comment,
                data=request.data,
                context={"request": request, "comment": comment},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=["comments"],
        request_body=CommentCreateSerializer,
    )
    def patch(self, request, id):
        try:
            comment = self.get_object(id)
            serializer = CommentCreateSerializer(
                comment,
                data=request.data,
                partial=True,
                context={"request": request, "comment": comment},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=["comments"])
    def delete(self, request, id):
        try:
            comment = self.get_object(id)
            comment.delete()
            return Response(
                {"detail": "Task deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
