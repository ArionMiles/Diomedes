from datetime import date, timedelta

from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Task

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