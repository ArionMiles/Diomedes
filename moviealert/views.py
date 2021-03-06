import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic.edit import UpdateView, CreateView, View
from django.views.generic import TemplateView
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
    form_class = modelform_factory(Profile, fields=['region'], 
                                            widgets={'region':Select2Widget},
                                            labels={'region': 'City'})
    template_name = "account/profile.html"

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        context['reminders'] = Reminder.objects.filter(user=self.request.user).order_by('-date')
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

    def get_initial(self):
        movie = self.request.GET.get('movie')
        initial = super(ReminderView, self).get_initial()
        initial['name'] = movie
        return initial

    def form_valid(self, form):
        model = form.save(commit=False)
        model.name = form.cleaned_data['name'].title()
        model.user = self.request.user
        
        if Reminder.objects.filter(user=model.user, name=model.name, language=model.language, 
                                                    dimension=model.dimension, date=model.date).exists():
            form.add_error(None, "This reminder already exists!")
            return self.form_invalid(form)
        model.save()
        for theater in form.cleaned_data['theaters'][:5]:
            TheaterLink.objects.create(reminder=model, theater=theater)
        return render(self.request, "success.html", {'obj': model})

class ReminderEditView(LoginRequiredMixin, RegionExistsMixin, UpdateView):
    form_class = ReminderForm
    model = Reminder
    template_name = "edit_reminder.html"

    def get_form_kwargs(self):
        kwargs = super(ReminderEditView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_object(self, queryset=None):
        obj = get_object_or_404(Reminder, id=self.kwargs['id'], user=self.request.user)
        return obj

    def form_valid(self, form):
        model = form.save(commit=False)
        model.name = form.cleaned_data['name'].title()
        model.user = self.request.user
        model.save()
        # Delete theaters which haven't opened sales yet
        TheaterLink.objects.filter(reminder=model, found=False).delete()

        for theater in form.cleaned_data['theaters'][:settings.MAX_THEATERS]:
            TheaterLink.objects.get_or_create(reminder=model, theater=theater)
        return render(self.request, "success.html", {'obj': model})

class AjaxMovieListView(View):
    def get(self, request):
        user_region = self.request.user.profile.region
        bms = BMS(user_region.code, user_region.name)
        data = bms.get_movie_list()
        data += bms.get_coming_soon(settings.BMS_TOKEN, 20, timezone.localdate())
        return JsonResponse({'movies': data, 'status':'ok'})

class TrendingView(LoginRequiredMixin, RegionExistsMixin, TemplateView):
    template_name = 'trending.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trends = BMS.get_trending(self.request.user.profile.region.code, settings.BMS_TOKEN)
        context['trending'] = trends
        return context

class DonateView(TemplateView):
    template_name = 'donate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donate_link'] = settings.DONATE_LINK
        return context