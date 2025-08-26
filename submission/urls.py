"""
File: urls.py
Author: Reagan Zierke
Date: 2025-07-16
Description: Django URL configuration for the submission app, including the path for submitting announcements.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_announcement, name='submit_announcement'),
    path('faq/', views.faq, name='faq'),
]