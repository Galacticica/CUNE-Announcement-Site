from django.shortcuts import render, redirect
from .forms import SubmissionForm



def submit_announcement(request):
    template_name = 'submission/submission.html'
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = SubmissionForm()
    return render(request, template_name, {'form': form})