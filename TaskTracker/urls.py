from django.contrib import admin
from django.urls import path, include

from TaskTracker.views import page_not_found, redirect_login, redirect_home
from users.views import logout_user

urlpatterns = [
    path('', redirect_home, name='index'),
    path('login', redirect_login, name='login'),
    path('logout', logout_user, name='logout'),
    path('admin/', admin.site.urls),
    path('users/', include(('users.urls', 'users'))),
    path('projects/', include(('tasks.urls', 'tasks'))),
]

handler404 = page_not_found
