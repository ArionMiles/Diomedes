import json

from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.views.generic.edit import UpdateView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms.models import modelform_factory
from django_select2.forms import Select2Widget
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.utils import timezone

from .forms import ReminderForm
from .models import Profile, Reminder, TheaterLink
from .BMS import BMS

class ProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = modelform_factory(Profile, 
                                    fields=['region'], 
                                    widgets={'region':Select2Widget},
                                    labels={'region': 'City'},
                                    )
    template_name = "account/profile.html"

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        context['reminders'] = Reminder.objects.filter(user=self.request.user)
        return context

class RegionExistsMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.profile.region

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('profile')

class ReminderView(LoginRequiredMixin, RegionExistsMixin, CreateView):
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
        
        if Reminder.objects.filter(user=model.user, name=model.name, language=model.language, dimension=model.dimension, date=model.date).exists():
            form.add_error(None, "This reminder already exists!")
            return self.form_invalid(form)
        model.save()
        for theater in form.cleaned_data['theaters'][:5]:
            TheaterLink.objects.create(reminder=model, theater=theater)
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

class AjaxMovieListView(View):
    def get(self, request):
        user_region = self.request.user.profile.region
        if self.request.is_ajax():
            bms = BMS(user_region.code, user_region.name)
            movie_list = bms.get_movie_list()
            movie_list += bms.get_coming_soon(settings.BMS_TOKEN, 20, timezone.localdate())
            movie_list = json.dumps(movie_list)
        else:
            movie_list = "This endpoint only responds to AJAX requests"
        mimetype = "application/json"
        return HttpResponse(movie_list, mimetype)
