"""
File: forms.py
Author: Reagan Zierke
Date: 2025-07-16
Description: Django forms for the Submission model, including validation.
"""



from django import forms
from django.core.exceptions import ValidationError
from .models import Submission

class SubmissionForm(forms.ModelForm):
    '''
    Form for creating and updating Submission instances.
    Validates that at least one of 'chapel' or 'praise' is selected
    and ensures that the start date is before the end date.
    '''

    class Meta:
        model = Submission
        fields = ['title', 'email', 'description', 'start_date', 'end_date', 'chapel', 'praise']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def clean(self):
        cleaned_data = super().clean()
        chapel = cleaned_data.get("chapel")
        praise = cleaned_data.get("praise")

        if not chapel and not praise:
            raise ValidationError("At least one of 'chapel' or 'praise' must be selected.")