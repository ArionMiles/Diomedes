from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import TaskForm
from .models import Task

def home_view(request):
    return render(request, "home.html")


@login_required
def task_view(request):
    form = TaskForm(request.POST or None)

    if request.method == 'POST':
        if request.user.is_authenticated:
            if form.is_valid():
                obj = form.save(commit=False)
                obj.movie_name = form.cleaned_data['movie_name'].title()
                obj.user = request.user
                obj.save()
                return render(request, "success.html", {'obj': obj})
            #messages.error(request, 'Something went wrong')
            return render(request, "add_task.html", {'form': form})
    else:
        ctx ={
            'form':form,
        }
        return render(request, "add_task.html", ctx)


def about_view(request):
    return render(request, "about.html")


@login_required
def user_profile(request):
    tasks = Task.objects.filter(user=request.user)
    ctx = {'user': request.user,
           'tasks': tasks}
    return render(request, "account/profile.html", ctx)

@login_required
def edit_task(request, id):
    instance = Task.objects.get(id=id)
    form = TaskForm(request.POST or None, instance=instance)

    if request.method == 'POST':
        if request.user.is_authenticated:
            if form.is_valid():
                obj = form.save(commit=False)
                obj.movie_name = form.cleaned_data['movie_name'].title()
                obj.user = request.user
                obj.save()
                return render(request, "success.html", {'obj': obj})
            return render(request, "edit_task.html", {'form': form})
    else:
        ctx ={
            'form':form,
            'task': instance,
        }
        return render(request, "edit_task.html", ctx)
