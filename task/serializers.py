from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Task, Comment
from user.models import User
from project.models import Project
from user.serializers import UserSerializer
from project.serializers import ProjectSerializer


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "project",
            "assigned_to",
            "due_date",
        ]

    def create(self, validated_data):
        project = self.context["project"]
        validated_data["project"] = project
        return super().create(validated_data)


class TaskCreateSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True
    )
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "project",
            "assigned_to",
            "due_date",
        ]

    def validate(self, data):
        project = self.context.get("project")

        if not project:
            task = self.context.get("task")
            if task:
                project = task.project

        if not project:
            raise serializers.ValidationError("Project does not exist.")

        if not project.members.filter(user_id=self.context["request"].user.id).exists():
            raise serializers.ValidationError("You are not a member of this project.")

        assigned_user = data.get("assigned_to")
        if assigned_user:
            is_member = project.members.filter(user_id=assigned_user.id).exists()
            if not is_member:
                raise serializers.ValidationError(
                    f"User {assigned_user.username} is not a member of this project."
                )

        self.context["project"] = project
        return data

    def create(self, validated_data):
        validated_data["project"] = self.context["project"]
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    task = TaskSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "content", "user", "task", "created_at"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep["user"] = {
            "id": instance.user.id,
            "username": instance.user.username,
        }

        if instance.task and instance.task.project:
            rep["task"] = {
                "id": instance.task.project.id,
                "title": instance.task.project.name,
                'assigned_to': {
                    'id': instance.task.assigned_to.id,
                    'username': instance.task.assigned_to.username,
                },
            }
        return rep


class CommentCreateSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["content", "task"]

    def validate(self, data):
        task = self.context.get('task')
        comment = self.context.get('comment')
        user = self.context['request'].user
        if task:
            if not task.project.members.filter(user=user).exists():
                raise serializers.ValidationError("You are not a member of this project.")
        if not task and not comment:
            raise serializers.ValidationError("Task or Comment does not exist.")
        return data
    
    def create(self, validated_data):
        validated_data["task"] = self.context["task"]
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
