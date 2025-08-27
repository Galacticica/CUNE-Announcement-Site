"""
File: views.py
Author: Reagan Zierke
Date: 2025-07-16
Description: Django views for handling submission of announcements, including form validation, image processing, and email notifications.
"""

from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from PIL import Image
from .forms import SubmissionForm
from .models import SubmissionSlide, Contact


def _validate_slide_extension(slide_name):
    """Validate that the slide has a valid image extension."""
    valid_extensions = ['.png', '.jpg', '.jpeg']
    return any(str(slide_name).lower().endswith(ext) for ext in valid_extensions)


def _validate_slide_aspect_ratio(image):
    """Validate that the slide has a 16:9 aspect ratio."""
    width, height = image.size
    aspect_ratio = width / height
    expected_ratio = 16 / 9
    return abs(aspect_ratio - expected_ratio) < 0.05


def _process_slides(request, form, submission):
    """Process uploaded slides with validation and save them."""
    error_found = False
    
    for slide in request.FILES.getlist('slides'):
        if not _validate_slide_extension(slide.name):
            form.add_error(None, f"{slide.name}: Slide must be a PNG or JPG image.")
            error_found = True
            continue
            
        try:
            img = Image.open(slide)
        except Exception:
            form.add_error(None, f"{slide.name}: Uploaded file is not a valid image.")
            error_found = True
            continue
            
        if not _validate_slide_aspect_ratio(img):
            form.add_error(None, f"{slide.name}: Slide must have a 16:9 aspect ratio.")
            error_found = True
            continue
            
        SubmissionSlide.objects.create(submission=submission, image=slide)
    
    return error_found


def _format_email_body(cleaned_data):
    """Format the email body with submission details."""
    start_date = cleaned_data.get("start_date")
    end_date = cleaned_data.get("end_date")
    formatted_start = start_date.strftime("%B %d, %Y") if start_date else "N/A"
    formatted_end = end_date.strftime("%B %d, %Y") if end_date else "N/A"
    
    return (
        f"Title: {cleaned_data.get('title', '')}\n"
        f"Contact Email: {cleaned_data.get('email', '')}\n"
        f"Description: {cleaned_data.get('description', '')}\n"
        f"Start Date: {formatted_start}\n"
        f"End Date: {formatted_end}\n"
    )


def _get_email_recipients(cleaned_data):
    """Get email recipients based on chapel and praise selections."""
    recipients = []
    # if cleaned_data.get("is_chapel"):
    #     chapel_people = Contact.objects.filter(is_chapel=True)
    #     recipients.extend([person.email for person in chapel_people])
    # if cleaned_data.get("is_praise"):
    #     praise_people = Contact.objects.filter(is_praise=True)
    #     recipients.extend([person.email for person in praise_people])
    praise_people = Contact.objects.filter(is_praise=True)
    recipients.extend([person.email for person in praise_people])
    return recipients


def _send_notification_email(cleaned_data, request):
    """Send email notification with submission details and attachments."""
    form_data = _format_email_body(cleaned_data)
    recipients = _get_email_recipients(cleaned_data)
    
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


def submit_announcement(request):
    """
    Handle announcement submission with form validation, image processing, and email notifications.
    """
    template_name = 'submission/submission.html'
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        
        if form.is_valid():
            submission = form.save()
            
            # Process and validate slides
            error_found = _process_slides(request, form, submission)
            
            if error_found:
                submission.delete()
                return render(request, template_name, {'form': form})
            
            # Send notification email
            _send_notification_email(form.cleaned_data, request)
            
            return redirect('/')
    else:
        form = SubmissionForm()
    
    return render(request, template_name, {'form': form})


def faq(request):
    """
    Render the FAQ page.
    """
    return render(request, 'submission/faq.html')