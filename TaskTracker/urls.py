from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template.context_processors import static
from django.urls import path, include
from django.views.generic import RedirectView

from TaskTracker.views import page_not_found, redirect_login, redirect_home
from users.views import logout_user

urlpatterns = [
    path('', redirect_home, name='index'),
    path('login', redirect_login, name='login'),
    path('logout', logout_user, name='logout'),
    path('admin/', admin.site.urls),
    path('users/', include(('users.urls', 'users'))),
    path('projects/', include(('tasks.urls', 'tasks'))),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("img/icons8-task-100.png")), name="favicon")
]

handler404 = page_not_found
