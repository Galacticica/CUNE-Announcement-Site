from django.contrib import admin
from .models import Submission, SubmissionSlide
from django.utils.html import format_html

class SubmissionSlideInline(admin.TabularInline):
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
    list_display = (
        'title',
        'email',
        'start_date_only',
        'end_date_only',
        'chapel',
        'praise',
        'first_slide_preview',
    )
    inlines = [SubmissionSlideInline]

    def start_date_only(self, obj):
        return obj.start_date.date() if obj.start_date else "-"
    start_date_only.short_description = "Start Date"

    def end_date_only(self, obj):
        return obj.end_date.date() if obj.end_date else "-"
    end_date_only.short_description = "End Date"

    def first_slide_preview(self, obj):
        first_slide = obj.slides.first() if hasattr(obj, "slides") else obj.submissionslide_set.first()
        if first_slide and first_slide.image:
            image_html = format_html('<img src="{}" style="max-height: 100px; margin-right:10px;"/>', first_slide.image.url)
            download_html = format_html('<a href="{}" download>Download</a>', first_slide.image.url)
            return format_html('{}{}', image_html, download_html)
        return "-"
    first_slide_preview.short_description = "Photo Preview"