from django.db import models
from user.models import TimeStampedModel, User
from project.models import Project


# Create your models here.
class Task(TimeStampedModel):
    STATUS_CHOICES = [
        ("TODO", "To Do"),
        ("IN_PROGRESS", "In Progress"),
        ("DONE", "Done"),
    ]

    PRIORITY_CHOICES = [("LOW", "Low"), ("MEDIUM", "Medium"), ("HIGH", "High")]

    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="TODO")
    priority = models.CharField(
        max_length=16, choices=PRIORITY_CHOICES, default="MEDIUM"
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks"
    )
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} | {self.status}"


class Comment(TimeStampedModel):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.user.username} -> {self.task.title}"
