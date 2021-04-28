"""
Trabajando con formularios
"""
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from .models import BookInstance


class RenewBookForm(forms.Form):
    """
    This class contains a form for setting the due_back for a book_instance
    This could be considered as a revewal
    """
    renewal_date = forms.DateField(
        required=True,
        help_text="Enter a date between now and 4 weeks (default 3)."
    )
    
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        
        #Check date is not in past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        
        #Check if date is in available range for a renewal (4 weeks)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Out of range - 4 weeks maximum'))
        
        return data#always return the cleaned_data
    
    
class RenewBookModelForm(ModelForm):
    """
    This class directly uses the Model for creating the form
    ModelForm will be very usefull with more than one field
    """    
    def clean_due_back(self):
        data = self.cleaned_data['due_back']
        
        #Check date is not in past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        
        #Check if date is in available range for a renewal (4 weeks)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        
        return data#always return the cleaned_data
    
    class Meta:
        model = BookInstance
        fields = ['due_back',]
        labels = {
            'due_back': _('renewal date'),
        }
        help_texts = {
            'due_back': _(
                'Enter a date between now and 4 weeks (default 3).'
            ),
        }