from django.shortcuts import render, redirect
from .forms import SubmissionForm
from .models import SubmissionSlide
from PIL import Image



def submit_announcement(request):
    template_name = 'submission/submission.html'
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save()
            error_found = False
            for slide in request.FILES.getlist('slides'):
                valid_extensions = ['.png', '.jpg', '.jpeg']
                if not any(str(slide.name).lower().endswith(ext) for ext in valid_extensions):
                    form.add_error(None, f"{slide.name}: Slide must be a PNG or JPG image.")
                    error_found = True
                    continue
                try:
                    img = Image.open(slide)
                except Exception:
                    form.add_error(None, f"{slide.name}: Uploaded file is not a valid image.")
                    error_found = True
                    continue
                width, height = img.size
                aspect_ratio = width / height
                expected_ratio = 16 / 9
                if not (abs(aspect_ratio - expected_ratio) < 0.05):
                    form.add_error(None, f"{slide.name}: Slide must have a 16:9 aspect ratio.")
                    error_found = True
                    continue
                SubmissionSlide.objects.create(submission=submission, image=slide)
            if error_found:
                # If any error, delete the submission and show errors
                submission.delete()
                return render(request, template_name, {'form': form})
            return redirect('/')
    else:
        form = SubmissionForm()
    return render(request, template_name, {'form': form})