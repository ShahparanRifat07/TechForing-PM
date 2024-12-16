from rest_framework import serializers
from .models import Project, ProjectMember
from user.models import User
from user.serializers import UserSerializer


class ProjectMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProjectMember
        fields = ["id", "project", "user", "created_at", "role"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if "user" in rep:
            rep["user"] = {
                "id": rep["user"]["id"],
                "name": f"{rep['user']['first_name']} {rep['user']['last_name']}".strip(),
            }
        rep.pop("project", None)
        return rep


class ProjectMemberCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(write_only=True)
    role = serializers.ChoiceField(choices=ProjectMember.ROLE_CHOICES, default="MEMBER")

    def validate(self, data):
        project = self.context["project"]
        user_id = data.get("user_id")

        if not user_id:
            raise serializers.ValidationError("User ID is required")

        if ProjectMember.objects.filter(project=project, user__id=user_id).exists():
            raise serializers.ValidationError(
                "User is already a member of this project"
            )

        return data

    def create(self, validated_data):
        try:
            project = self.context["project"]
            user = User.objects.get(id=validated_data["user_id"])
            validated_data["user"] = user
            validated_data["project"] = project
            return ProjectMember.objects.create(**validated_data)
        except Exception as e:
            return serializers.ValidationError(
                {"error": "Failed to add user to project"}
            )


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    members = ProjectMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "owner", "created_at", "members"]

    def create(self, validated_data):
        try:
            owner = self.context["request"].user
            project = Project.objects.create(owner=owner, **validated_data)
            ProjectMember.objects.create(project=project, user=owner, role="ADMIN")
            return project

        except Exception as e:
            raise serializers.ValidationError({"error": "Failed to create project"})

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if "owner" in rep:
            rep["owner"] = {
                "id": rep["owner"]["id"],
                "name": f"{rep['owner']['first_name']} {rep['owner']['last_name']}".strip(),
            }

        return rep
