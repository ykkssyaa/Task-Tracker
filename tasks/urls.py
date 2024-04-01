from django.urls import path

from tasks import views

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('add_project', views.AddProjectView.as_view(), name='add_project'),
    path('<int:pk>/add_task', views.AddTaskView.as_view(), name='add_task'),
    path('<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),
    #path('tasks/<int:pk>', views.TaskDetailView.as_view(), name='task_detail'),
]
