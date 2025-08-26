"""
File: admin.py
Author: Reagan Zierke
Date: 2025-07-16
Description: Django admin configuration for the Submission model, including inline management of SubmissionSlide objects, custom display fields, and deletion functionality.
"""

from django.contrib import admin
from .models import Submission, SubmissionSlide, Contact
from django.utils.html import format_html
from django.utils import timezone


admin.site.site_header = "CUNE Announcements Admin"
admin.site.site_title = "CUNE Announcements Admin"
admin.site.index_title = "CUNE Announcements Administration"

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_chapel', 'is_praise')

class SubmissionSlideInline(admin.TabularInline):
    '''
    Inline admin for SubmissionSlide model to manage slides associated with a Submission.
    Provides fields for image upload, preview, and download link.
    '''

    model = SubmissionSlide
    extra = 0
    readonly_fields = ('image_preview', 'download_link')
    fields = ('image', 'image_preview', 'download_link')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"

    def download_link(self, obj):
        if obj.image:
            return format_html('<a href="{}" download>Download</a>', obj.image.url)
        return "-"
    download_link.short_description = "Download"

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    '''
    Admin configuration for Submission model.
    '''

    list_display = (
        'title',
        'email',
        'start_date_only',
        'end_date_only',
        'is_chapel',
        'is_praise',
        'all_slides_preview', 
        'is_active',
        'delete_announcement',  
    )
    inlines = [SubmissionSlideInline]

    def start_date_only(self, obj):
        return obj.start_date.date() if obj.start_date else "-"
    start_date_only.short_description = "Start Date"

    def end_date_only(self, obj):
        return obj.end_date.date() if obj.end_date else "-"
    end_date_only.short_description = "End Date"

    def all_slides_preview(self, obj):
        '''
        Returns a formatted HTML string with previews and download links for all slides associated with the submission.
        '''

        slides = obj.slides.all() if hasattr(obj, "slides") else obj.submissionslide_set.all()
        if slides:
            html = ""
            for slide in slides:
                if slide.image:
                    image_html = format_html(
                        '<img src="{}" style="max-height: 100px; margin-right:10px;"/>',
                        slide.image.url
                    )
                    download_html = format_html(
                        '<a href="{}" download>Download</a>',
                        slide.image.url
                    )
                    html += format_html('{}{}<br>', image_html, download_html)
            return format_html(html)
        return "-"
    all_slides_preview.short_description = "Photo Previews"

    def is_active(self, obj):
        '''
        Checks if the submission is currently active based on the start and end dates.
        Returns True if the current date is within the start and end dates, otherwise False.
        '''

        now = timezone.now().date()
        start = obj.start_date.date() if obj.start_date else None
        end = obj.end_date.date() if obj.end_date else None
        if start and end:
            return start <= now <= end
        return False
    is_active.boolean = True
    is_active.short_description = "Active"
    is_active.admin_order_field = 'start_date'

    def delete_announcement(self, obj):
        delete_url = f"/admin/submission/submission/{obj.id}/delete/"
        return format_html(
            '<a href="{}" style="color:red;">Delete</a>',
            delete_url
        )
    delete_announcement.short_description = "Delete"
    

