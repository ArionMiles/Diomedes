from datetime import date, timedelta

from django.utils.translation import gettext_lazy as _
from django import forms
from django_select2.forms import Select2MultipleWidget

from .models import Task, Reminder, Theater

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['movie_name', 'city', 'movie_language', 'movie_dimension', 'movie_date']
        labels = {
            'movie_name': _('Movie'),
            'movie_language': _('Language'),
            'movie_dimension': _('Dimension'),
            'movie_date': _('Date'),
        }
        help_texts = {
            'movie_name': "Try to name the movie as close to what it is on BMS",
            # 'movie_language': "",
            # 'movie_dimension': "",
            'movie_date': "Release date or after",
        }
        widgets = {
            'movie_date': forms.DateInput(attrs={
                                                'type':'date',
                                                }),
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['movie_date'].widget.attrs['min'] = date.today() + timedelta(days=1)

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['name', 'language', 'dimension', 'date', 'theaters']
        labels = {
            'name': _('Movie'),
        }
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'}),
            'theaters': Select2MultipleWidget({'data-maximum-selection-length': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ReminderForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['min'] = date.today() + timedelta(days=1)
        self.fields['theaters'].queryset = Theater.objects.filter(subregion=self.request.user.profile.subregion)
