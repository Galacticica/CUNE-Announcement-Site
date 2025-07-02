from django.db import models

class Submission(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title', help_text='Enter the title of the announcement')
    email = models.EmailField(max_length=254, verbose_name='Contact Email', help_text='Enter the email address to contact for any questions', blank=True, null=True)
    description = models.TextField(verbose_name='Description', help_text='Enter the description of the announcement')
    start_date = models.DateTimeField(verbose_name='Start Date', help_text='Enter the start date of the announcement')
    end_date = models.DateTimeField(verbose_name='End Date', help_text='Enter the end date of the announcement')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At', help_text='The date and time when the announcement was created')
    chapel = models.BooleanField(default=False, verbose_name='Chapel', help_text='Indicates if the announcement is for chapel')
    praise = models.BooleanField(default=False, verbose_name='Praise', help_text='Indicates if the announcement is for praise')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
        ordering = ['-start_date']

class SubmissionSlide(models.Model):
    submission = models.ForeignKey('Submission', on_delete=models.CASCADE, related_name='slides')
    image = models.ImageField(upload_to='announcements/')

    def __str__(self):
        return f"Slide for {self.submission.title}"
