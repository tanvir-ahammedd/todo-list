from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Task
from .forms import TaskForm

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    
class RegisterPage(FormView):
    form_class = UserCreationForm
    template_name = "base/register.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        user = form.save()
        
        # dont need to login after register, automatically login
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    # login user cant go to register page, will redirect to tasks
    def get(self, args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
    

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

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy('tasks')
    
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "base/delete_task.html"
    context_object_name = 'delete'
    success_url = reverse_lazy("tasks")
    