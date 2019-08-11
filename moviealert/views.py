from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import modelform_factory
from django_select2.forms import Select2Widget

from .forms import TaskForm, ReminderForm
from .models import Task, Profile, Reminder, TheaterLink

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

        
@login_required
def user_profile(request):
    tasks = Task.objects.filter(user=request.user)
    ctx = {'user': request.user,
           'tasks': tasks}
    return render(request, "account/profile.html", ctx)

@login_required
def edit_task(request, id):
    try:
        instance = Task.objects.get(id=id, user=request.user)
    except Task.DoesNotExist:
        raise Http404("No such record found")
    
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

class ProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = modelform_factory(Profile, 
                                    fields=['subregion'], 
                                    widgets={'subregion':Select2Widget},
                                    labels={'subregion': 'City'},
                                    )
    template_name = "account/profile.html"

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

class ReminderView(LoginRequiredMixin, CreateView):
    form_class = ReminderForm
    model = Reminder
    template_name = "reminder.html"

    def get_form_kwargs(self):
        kwargs = super(ReminderView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        model = form.save(commit=False)
        model.name = form.cleaned_data['name'].title()
        model.user = self.request.user
        model.save()
        for theater in form.cleaned_data['theaters'][:5]:
            TheaterLink.objects.create(reminder=model, theater=theater)
        # form.save_m2m() # Saving m2m relations, refer ModelForm doc to understand why
        return render(self.request, "success.html", {'obj': model})

class ReminderEditView(LoginRequiredMixin, UpdateView):
    form_class = ReminderForm
    model = Reminder
    template_name = "edit_reminder.html"

    def get_form_kwargs(self):
        kwargs = super(ReminderEditView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_object(self, queryset=None):
        return Reminder.objects.get(id=self.kwargs['id'])
    
    def form_valid(self, form):
        model = form.save(commit=False)
        model.name = form.cleaned_data['name'].title()
        model.user = self.request.user
        model.save()
        TheaterLink.objects.filter(reminder=model).delete()
        for theater in form.cleaned_data['theaters'][:5]:
            TheaterLink.objects.create(reminder=model, theater=theater)
        return render(self.request, "success.html", {'obj': model})