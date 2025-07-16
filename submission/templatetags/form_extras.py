"""
File: form_extras.py
Author: Reagan Zierke
Date: 2025-07-16
Description: Custom template filters for forms, including adding CSS classes to form fields.
"""

from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})