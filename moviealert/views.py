from django.shortcuts import render
from django.http import Http404
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import modelform_factory
from django_select2.forms import Select2Widget

from .forms import ReminderForm
from .models import Profile, Reminder, TheaterLink

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

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        context['reminders'] = Reminder.objects.filter(user=self.request.user)
        return context

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
        try:
            obj = Reminder.objects.get(id=self.kwargs['id'], user=self.request.user)
        except Reminder.DoesNotExist:
            raise Http404()
        return obj
    
    def form_valid(self, form):
        model = form.save(commit=False)
        model.name = form.cleaned_data['name'].title()
        model.user = self.request.user
        model.save()
        TheaterLink.objects.filter(reminder=model, found=False).delete() # Delete theaters which haven't opened sales yet
        for theater in form.cleaned_data['theaters'][:5]:
            t, created = TheaterLink.objects.get_or_create(reminder=model, theater=theater)
            t.save()
        return render(self.request, "success.html", {'obj': model})