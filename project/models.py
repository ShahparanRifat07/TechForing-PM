from django.db import models
from user.models import TimeStampedModel, User

# Create your models here.
class Project(TimeStampedModel):
    name = models.CharField(max_length=128)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_projects")

    def __str__(self):
        return self.name


class ProjectMember(TimeStampedModel):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('MEMBER', 'Member')
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="project_members")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES,default='MEMBER')

    class Meta:
        unique_together = ('project', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.project.name}"