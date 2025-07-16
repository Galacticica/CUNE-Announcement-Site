"""
File: urls.py
Author: Reagan Zierke
Date: 2025-07-16
Description: Django URL configuration for the project, including admin routes, browser reload, and app-specific URLs.
"""


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("", include("submission.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
