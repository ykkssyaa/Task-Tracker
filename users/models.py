from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    TEAMLEAD = 'teamlead'
    DIRECTOR = 'director'
    DEVELOPER = 'developer'

    ROLE_CHOICES = [
        (TEAMLEAD, 'Team Lead'),
        (DIRECTOR, 'Director'),
        (DEVELOPER, 'Developer'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=DEVELOPER)

    def __str__(self):
        return self.username
