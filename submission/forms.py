from django import forms
from django.core.exceptions import ValidationError
from .models import Submission

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['title', 'email', 'description', 'start_date', 'end_date', 'chapel', 'praise']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        chapel = cleaned_data.get("chapel")
        praise = cleaned_data.get("praise")

        if not chapel and not praise:
            raise ValidationError("At least one of 'chapel' or 'praise' must be selected.")