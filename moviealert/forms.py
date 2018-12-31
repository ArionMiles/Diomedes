from django import forms
from .models import Task
class TaskForm(forms.ModelForm):
    model = Task
    fields = ['movie_name', 'city', 'movie_language', 'movie_dimension', 'movie_date']