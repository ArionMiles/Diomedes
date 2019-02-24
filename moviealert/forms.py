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