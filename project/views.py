from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from drf_yasg.utils import swagger_auto_schema

from .models import Project
from .serializers import (
    ProjectSerializer,
    ProjectMemberSerializer,
    ProjectMemberCreateSerializer,
)
from .permissions import IsProjectOwnerOrAdmin


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsProjectOwnerOrAdmin]

    def get_queryset(self):
        return Project.objects.filter(members__user=self.request.user)

    @swagger_auto_schema(
        request_body=ProjectMemberCreateSerializer,
        responses={201: ProjectMemberSerializer},
    )
    @action(
        detail=True,
        methods=["POST"],
        permission_classes=[IsAuthenticated, IsProjectOwnerOrAdmin],
    )
    def add_member(self, request, pk=None):

        project = self.get_object()

        if not project.is_owner_or_admin(request.user):
            raise PermissionDenied("Only project owners or admins can add members")

        try:
            data = {
                "user_id": request.data.get("user_id"),
                "role": request.data.get("role", "MEMBER"),
            }
            serializer = ProjectMemberCreateSerializer(
                data=data, context={"request": request, "project": project}
            )
            serializer.is_valid(raise_exception=True)
            member = serializer.save()

            return Response(
                ProjectSerializer(project).data, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
