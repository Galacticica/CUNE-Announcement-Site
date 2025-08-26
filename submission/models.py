"""
File: models.py
Author: Reagan Zierke
Date: 2025-07-16
Description: Django models for the Submission and SubmissionSlide
"""


from django.db import models

class Submission(models.Model):
    '''
    Model representing an announcement submission.
    Contains fields for title, email, description, start and end dates,
    and flags for chapel and praise announcements.
    Provides methods for string representation and metadata configuration.
    '''

    title = models.CharField(max_length=200, verbose_name='Title', help_text='Enter the title of the announcement')
    email = models.EmailField(max_length=254, verbose_name='Contact Email', help_text='Enter the email address to contact for any questions', blank=True, null=True)
    description = models.TextField(verbose_name='Description', help_text='Enter the description of the announcement', blank=True, null=True)
    start_date = models.DateTimeField(verbose_name='Start Date', help_text='Enter the start date of the announcement')
    end_date = models.DateTimeField(verbose_name='End Date', help_text='Enter the end date of the announcement')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At', help_text='The date and time when the announcement was created')
    chapel = models.BooleanField(default=False, verbose_name='Chapel', help_text='Indicates if the announcement is for chapel')
    praise = models.BooleanField(default=True, verbose_name='Praise', help_text='Indicates if the announcement is for praise')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
        ordering = ['-start_date']

class SubmissionSlide(models.Model):
    '''
    Model representing a slide associated with a submission.
    Contains a foreign key to the Submission model and an image field for the slide image.
    '''

    submission = models.ForeignKey('Submission', on_delete=models.CASCADE, related_name='slides')
    image = models.ImageField(upload_to='announcements/')

    def __str__(self):
        return f"Slide for {self.submission.title}"


class Contact(models.Model):
    """
    Model representing who to contact when submitted
    """

    name = models.CharField(max_length=100, verbose_name='Name', help_text='Enter the name of the contact person')
    email = models.EmailField(max_length=254, verbose_name='Email', help_text='Enter the email address of the contact person')
    is_chapel = models.BooleanField(default=False, verbose_name='Chapel Contact', help_text='Indicates if this contact is for chapel announcements')
    is_praise = models.BooleanField(default=False, verbose_name='Praise Contact', help_text='Indicates if this contact is for praise announcements')