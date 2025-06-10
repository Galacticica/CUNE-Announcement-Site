from django import forms
from .models import Submission
from PIL import Image

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['title', 'email', 'description', 'start_date', 'end_date', 'slide', 'chapel', 'praise']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_slide(self):
        slide = self.cleaned_data.get('slide')
        if slide:

            valid_extensions = ['.png', '.jpg', '.jpeg']
            if not any(str(slide.name).lower().endswith(ext) for ext in valid_extensions):
                raise forms.ValidationError("Slide must be a PNG or JPG image.")
            try:
                img = Image.open(slide)
                width, height = img.size
                aspect_ratio = width / height
                expected_ratio = 16 / 9
                if not (abs(aspect_ratio - expected_ratio) < 0.05):
                    raise forms.ValidationError("Slide must have a 16:9 aspect ratio.")
            except Exception:
                raise forms.ValidationError("Uploaded file is not a valid image.")
        return slide

