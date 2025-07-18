from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "base/details.html"
    context_object_name = "task"

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy('tasks')

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy('tasks')
    
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "base/delete_task.html"
    context_object_name = 'delete'
    success_url = reverse_lazy("tasks")
    