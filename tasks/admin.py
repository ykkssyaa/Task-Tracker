from django.contrib import admin
import tasks.models as models

admin.site.register(models.Project)
admin.site.register(models.Task)
