from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        return context
    
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "base/details.html"
    context_object_name = "task"

#option 1
# class TaskCreate(LoginRequiredMixin, CreateView):
#     model = Task
#     fields = ['title', 'description', 'complete']
#     success_url = reverse_lazy('tasks')
    
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
    
# option 2
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy('tasks')
    
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "base/delete_task.html"
    context_object_name = 'delete'
    success_url = reverse_lazy("tasks")
    