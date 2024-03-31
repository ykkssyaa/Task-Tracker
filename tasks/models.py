from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)

    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')

    def __str__(self):
        return self.name

