from django.contrib import admin
from .models import Submission, SubmissionSlide
from django.utils.html import format_html
from django.utils import timezone

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
        'all_slides_preview', 
        'is_active',
    )
    inlines = [SubmissionSlideInline]

    def start_date_only(self, obj):
        return obj.start_date.date() if obj.start_date else "-"
    start_date_only.short_description = "Start Date"

    def end_date_only(self, obj):
        return obj.end_date.date() if obj.end_date else "-"
    end_date_only.short_description = "End Date"

    def all_slides_preview(self, obj):
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
        now = timezone.now().date()
        start = obj.start_date.date() if obj.start_date else None
        end = obj.end_date.date() if obj.end_date else None
        if start and end:
            return start <= now <= end
        return False
    is_active.boolean = True
    is_active.short_description = "Active"
    is_active.admin_order_field = 'start_date'