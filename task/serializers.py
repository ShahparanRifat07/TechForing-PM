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
        fields = ['id', 'title', 'description', 'status', 'priority', 'project', 'assigned_to', 'due_date']

    def create(self, validated_data):
        project = self.context['project']
        validated_data['project'] = project
        return super().create(validated_data)



class TaskCreateSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'project', 'assigned_to', 'due_date']

    def validate(self, data):
        project = self.context.get('project')

        if not project:
            task = self.context.get('task')
            if task:
                project = task.project

        if not project:
            raise serializers.ValidationError("Project does not exist.")

        if not project.members.filter(user_id=self.context['request'].user.id).exists():
            raise serializers.ValidationError("You are not a member of this project.")
        
        assigned_user = data.get('assigned_to')
        if assigned_user:
            is_member = project.members.filter(user_id=assigned_user.id).exists()
            if not is_member:
                raise serializers.ValidationError(
                    f"User {assigned_user.username} is not a member of this project."
                )
            
        self.context['project'] = project
        return data

    def create(self, validated_data):
        validated_data['project'] = self.context['project']
        return super().create(validated_data)

