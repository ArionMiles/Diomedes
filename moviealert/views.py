from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TaskForm
from .models import Task
# Create your views here.

def TaskView(request):
    form = TaskForm(request.POST or None)

    if request.method == 'POST':
        if request.user.is_authenticated:
            if form.is_valid():
                obj = form.save(commit=False)
                obj.username = request.user.email
                obj.save()
                # Redirect to success page maybe?
                return redirect('home')
            #messages.error(request, 'Something went wrong')
            return render(request, "home.html", {'form':form})
    else:
        ctx ={
            'form':form,
        }
        return render(request, "home.html", ctx)