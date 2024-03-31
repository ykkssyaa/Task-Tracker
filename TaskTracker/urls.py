from django.contrib import admin
from django.urls import path, include

from TaskTracker.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(('users.urls', 'users'))),
    path('tasks/', include(('tasks.urls', 'tasks'))),
]

handler404 = page_not_found
