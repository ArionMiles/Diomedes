from datetime import date, timedelta

from django.utils.translation import gettext_lazy as _
from django import forms
from django_select2.forms import Select2MultipleWidget

from .models import Reminder, Theater

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
