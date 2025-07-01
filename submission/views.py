from django.shortcuts import render, redirect
from .forms import SubmissionForm
from .models import SubmissionSlide
from PIL import Image
from django.core.mail import EmailMessage  



def submit_announcement(request):
    template_name = 'submission/submission.html'
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
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
                submission.delete()
                return render(request, template_name, {'form': form})

            cleaned = form.cleaned_data
            start_date = cleaned.get("start_date")
            end_date = cleaned.get("end_date")
            formatted_start = start_date.strftime("%B %d, %Y") if start_date else "N/A"
            formatted_end = end_date.strftime("%B %d, %Y") if end_date else "N/A"
            form_data = (
                f"Title: {cleaned.get('title', '')}\n"
                f"Email: {cleaned.get('email', '')}\n"
                f"Description: {cleaned.get('description', '')}\n"
                f"Start Date: {formatted_start}\n"
                f"End Date: {formatted_end}\n"
            )
            recipients = []
            if cleaned.get("chapel"):
                recipients.append("ojthecat127@gmail.com")
            if cleaned.get("praise"):
                recipients.append("reaganzierke@gmail.com")

            email = EmailMessage(
                subject="New Announcement",
                body=f"A new announcement has been submitted:\n\n{form_data}",
                from_email="reaganzierke@gmail.com",
                to=recipients,
            )
            for slide in request.FILES.getlist('slides'):
                slide.open()
                email.attach(slide.name, slide.read(), slide.content_type)
            email.send()

            return redirect('/')
    else:
        form = SubmissionForm()
    return render(request, template_name, {'form': form})