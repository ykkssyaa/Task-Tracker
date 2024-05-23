import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView

from tasks.forms import TaskForm, ProjectForm
from tasks.models import Project, Task
from users.models import User


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


class UpdateProjectView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'tasks/add_project.html'
    context_object_name = 'task'

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обновление проекта'
        context['edit'] = 1

        return context


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


class UpdateTaskView(UpdateView):
    model = Task
    template_name = 'tasks/add_task.html'
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy('tasks:project_detail', kwargs={'pk': self.object.project.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обновление задачи'
        context['edit'] = 1

        return context




def update_status(request, task_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_status = data.get('status')
        task = Task.objects.get(id=task_id)
        task.status = new_status
        task.save()
        return JsonResponse({'success': True}, status=200)
    return JsonResponse({'success': False})


def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        task.delete()
        return JsonResponse({'success': True})
    except Task.DoesNotExist:
        return JsonResponse({'success': False}, status=404)


def project_statistics(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Получаем общее количество задач в проекте
    total_tasks = project.task_set.count()

    # Получаем количество выполненных задач в проекте
    completed_tasks = project.task_set.filter(status='completed').count()

    # Получаем количество разработчиков на проекте
    num_developers = project.task_set.values('owner').distinct().count()

    # Получаем тимлида проекта
    project_lead = project.owner

    # Вычисляем общий процент выполненных задач в проекте
    if total_tasks > 0:
        completion_percentage = (completed_tasks / total_tasks) * 100
    else:
        completion_percentage = 0

    # Получаем количество не завершенных задач для каждого пользователя с ролью developer на проекте
    developers = User.objects.filter(role='developer', task__project=project).annotate(
        total_tasks=Count('task'),
        num_incomplete_tasks=Count('task', filter=Q(task__status='todo') | Q(task__status='in_progress'))
    )
    for developer in developers:
        if developer.total_tasks > 0:
            developer.completion_percentage = ((developer.total_tasks - developer.num_incomplete_tasks) / developer.total_tasks) * 100
        else:
            developer.completion_percentage = 0

    context = {
        'project': project,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'num_developers': num_developers,
        'completion_percentage': completion_percentage,
        'developers': developers,
        'project_lead': project_lead,
        'title': 'Статистика проекта'
    }

    return render(request, 'tasks/statistics.html', context)
