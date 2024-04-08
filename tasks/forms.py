from django.forms import ModelForm, ModelChoiceField, DateField, DateInput

from tasks.models import Task, Project
from users.models import User


class TaskForm(ModelForm):
    owner = ModelChoiceField(queryset=User.objects.filter(role='developer'), label='Исполнитель')
    start_date = DateField(widget=DateInput(attrs={'type': 'date'}), label='Дата начала', required=False)
    end_date = DateField(widget=DateInput(attrs={'type': 'date'}), label='Дата окончания')

    class Meta:
        model = Task
        fields = ['name', 'description', 'start_date', 'end_date', 'priority', 'owner']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'start_date': 'Дата начала',
            'end_date': 'Дата окончания',
            'priority': 'Приоритет',
        }

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        if 'instance' in kwargs:
            task = kwargs['instance']
            initial['start_date'] = task.start_date
            initial['end_date'] = task.end_date
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

class ProjectForm(ModelForm):
    owner = ModelChoiceField(queryset=User.objects.filter(role='teamlead'), label='Team Lead')

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'start_date': 'Дата начала',
            'end_date': 'Дата окончания',
        }
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        if 'instance' in kwargs:
            project = kwargs['instance']
            initial['start_date'] = project.start_date
            initial['end_date'] = project.end_date
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)