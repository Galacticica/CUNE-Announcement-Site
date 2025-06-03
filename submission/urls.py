from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_announcement, name='submit_announcement')
]