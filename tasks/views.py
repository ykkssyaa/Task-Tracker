from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, FormView, CreateView

from tasks.forms import TaskForm, ProjectForm
from tasks.models import Project, Task


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'tasks/project_page.html'
    context_object_name = 'project'
    extra_context = {'title': 'Страница проекта'}


class ProjectListView(ListView):
    model = Project
    template_name = 'tasks/project_list.html'
    context_object_name = 'projects'
    extra_context = {'title': 'Список проектов'}


class AddProjectView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'tasks/add_project.html'
    extra_context = {'title': 'Добавление нового проекта'}

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


class AddTaskView(FormView):
    template_name = 'tasks/add_task.html'
    form_class = TaskForm

    def form_valid(self, form):
        project = Project.objects.get(pk=self.kwargs['pk'])  # Получаем объект проекта по его pk
        form.instance.project = project
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Формируем URL для страницы деталей задачи с использованием идентификатора
        return reverse('tasks:project_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем проект по его pk
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        # Добавляем проект в контекст
        context['project'] = project
        context['title'] = f'Добавление задачи для {project.name}'

        return context


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    extra_context = {'title': 'Список задач'}

    def get_queryset(self):
        user = self.request.user
        if user.role == 'director':
            # Вывести все задачи для директора
            return Task.objects.all()
        elif user.role == 'teamlead':
            # Вывести задачи только для проектов, где пользователь - тимлид
            return Task.objects.filter(project__owner=user)
        else:
            # Вывести задачи, где пользователь - owner
            return Task.objects.filter(owner=user)
