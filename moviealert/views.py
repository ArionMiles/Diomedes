from django.shortcuts import render
from .forms import TaskForm
from .models import Task
# Create your views here.

def TaskView(request):
    form = TaskForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # Redirect to success page maybe?
    
    ctx ={
        'form':form,
    }

    return render(request, "home.html", ctx)