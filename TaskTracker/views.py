from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found 404</h1> <a href='/'>На главную страницу</a>")


def redirect_home(request):
    return HttpResponseRedirect(reverse('tasks:project_list'))


def redirect_login(request):
    return HttpResponseRedirect(reverse('users:login'))
