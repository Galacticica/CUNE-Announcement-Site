# Generated by Django 5.2.1 on 2025-06-10 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0003_submission_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='name',
        ),
        migrations.AddField(
            model_name='submission',
            name='email',
            field=models.EmailField(blank=True, help_text='Enter the email address for the announcement', max_length=254, null=True, verbose_name='Email'),
        ),
    ]
