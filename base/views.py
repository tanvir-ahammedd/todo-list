from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Task

class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'
    
class TaskDetail(DetailView):
    model = Task
    template_name = "base/details.html"
    context_object_name = "task"

class TaskCreate(CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy('tasks')
    