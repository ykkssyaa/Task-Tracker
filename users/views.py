from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from users.forms import LoginUserForm
from users.models import User


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))


class UserList(ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'
    extra_context = {'title': 'Список пользователей'}


class UserPage(DetailView):
    model = User
    template_name = 'users/user_page.html'
    context_object_name = 'user_p'

    def get_object(self, queryset=None):
        username = self.kwargs['username']
        # Получаем объект пользователя по его имени пользователя (username)
        return get_object_or_404(User, username=username, is_superuser=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        context['title'] = f'Профиль {username}'
        return context

