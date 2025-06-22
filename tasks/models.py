from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    STATUS_CHOICES = [
        ("new", "Новая"),
        ("in_progress", "В процессе"),
        ("done", "Выполнено"),
    ]

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='user_tasks',
        verbose_name="автор задачи"
    )
    title = models.CharField("название задачи", max_length=30)
    description = models.TextField("описание задачи", blank=True)
    due_date = models.DateField("дедлайн задачи")
    status = models.CharField("статус задачи", choices=STATUS_CHOICES, default="new", max_length=20)

    @property
    def is_overdue(self):
        return self.due_date < timezone.now().date() and self.status != 'done'

    def __str__(self):
        return self.title

