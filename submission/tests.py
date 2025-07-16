"""
File: tests.py
Author: Reagan Zierke
Date: 2025-07-16
Description: Tests for submitting announcements.
"""

import io
from datetime import datetime, timedelta
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail
from django.core.exceptions import ValidationError
from PIL import Image
from .models import Submission, SubmissionSlide
from .forms import SubmissionForm


class SubmissionModelTest(TestCase):
    """Test cases for the Submission model."""
    
    def setUp(self):
        """Set up test data."""
        self.valid_data = {
            'title': 'Test Announcement',
            'email': 'test@example.com',
            'description': 'This is a test announcement',
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=7),
            'chapel': True,
            'praise': False
        }
    
    def test_submission_creation(self):
        """Test creating a submission with valid data."""
        submission = Submission.objects.create(**self.valid_data)
        
        self.assertEqual(submission.title, 'Test Announcement')
        self.assertEqual(submission.email, 'test@example.com')
        self.assertEqual(submission.description, 'This is a test announcement')
        self.assertTrue(submission.chapel)
        self.assertFalse(submission.praise)
        self.assertIsNotNone(submission.created_at)
    
    def test_submission_str_method(self):
        """Test the string representation of a submission."""
        submission = Submission.objects.create(**self.valid_data)
        self.assertEqual(str(submission), 'Test Announcement')
    
    def test_submission_ordering(self):
        """Test that submissions are ordered by start_date descending."""
        submission1 = Submission.objects.create(
            title='First',
            description='First announcement',
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            chapel=True
        )
        submission2 = Submission.objects.create(
            title='Second',
            description='Second announcement',
            start_date=datetime.now() + timedelta(days=1),
            end_date=datetime.now() + timedelta(days=2),
            chapel=True
        )
        
        submissions = Submission.objects.all()
        self.assertEqual(submissions[0], submission2)  # More recent start_date first
        self.assertEqual(submissions[1], submission1)


class SubmissionSlideModelTest(TestCase):
    """Test cases for the SubmissionSlide model."""
    
    def setUp(self):
        """Set up test data."""
        self.submission = Submission.objects.create(
            title='Test Announcement',
            description='Test description',
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=7),
            chapel=True
        )
    
    def test_submission_slide_creation(self):
        """Test creating a submission slide."""
        # Create a simple test image
        image = self._create_test_image()
        
        slide = SubmissionSlide.objects.create(
            submission=self.submission,
            image=image
        )
        
        self.assertEqual(slide.submission, self.submission)
        self.assertIsNotNone(slide.image)
    
    def test_submission_slide_str_method(self):
        """Test the string representation of a submission slide."""
        image = self._create_test_image()
        slide = SubmissionSlide.objects.create(
            submission=self.submission,
            image=image
        )
        
        self.assertEqual(str(slide), 'Slide for Test Announcement')
    
    def test_submission_slide_cascade_delete(self):
        """Test that slides are deleted when submission is deleted."""
        image = self._create_test_image()
        slide = SubmissionSlide.objects.create(
            submission=self.submission,
            image=image
        )
        
        slide_id = slide.id
        self.submission.delete()
        
        self.assertFalse(SubmissionSlide.objects.filter(id=slide_id).exists())
    
    def _create_test_image(self):
        """Helper method to create a test image file."""
        image = Image.new('RGB', (1920, 1080), color='red')  # 16:9 aspect ratio
        image_io = io.BytesIO()
        image.save(image_io, format='PNG')
        image_io.seek(0)
        
        return SimpleUploadedFile(
            name='test_image.png',
            content=image_io.getvalue(),
            content_type='image/png'
        )


class SubmissionFormTest(TestCase):
    """Test cases for the SubmissionForm."""
    
    def setUp(self):
        """Set up test data."""
        self.valid_data = {
            'title': 'Test Announcement',
            'email': 'test@example.com',
            'description': 'This is a test announcement',
            'start_date': '2025-07-16',
            'end_date': '2025-07-23',
            'chapel': True,
            'praise': False
        }
    
    def test_form_valid_data(self):
        """Test form with valid data."""
        form = SubmissionForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
    
    def test_form_missing_required_fields(self):
        """Test form with missing required fields."""
        incomplete_data = self.valid_data.copy()
        del incomplete_data['title']
        
        form = SubmissionForm(data=incomplete_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_form_neither_chapel_nor_praise_selected(self):
        """Test form validation when neither chapel nor praise is selected."""
        invalid_data = self.valid_data.copy()
        invalid_data['chapel'] = False
        invalid_data['praise'] = False
        
        form = SubmissionForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("At least one of 'chapel' or 'praise' must be selected.", form.non_field_errors())
    
    def test_form_both_chapel_and_praise_selected(self):
        """Test form is valid when both chapel and praise are selected."""
        data = self.valid_data.copy()
        data['chapel'] = True
        data['praise'] = True
        
        form = SubmissionForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_form_only_praise_selected(self):
        """Test form is valid when only praise is selected."""
        data = self.valid_data.copy()
        data['chapel'] = False
        data['praise'] = True
        
        form = SubmissionForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_email_format(self):
        """Test form validation with invalid email format."""
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = 'invalid-email'
        
        form = SubmissionForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class SubmissionViewTest(TestCase):
    """Test cases for the submission view."""
    
    def setUp(self):
        """Set up test client and data."""
        self.client = Client()
        self.url = reverse('submit_announcement')
        self.valid_data = {
            'title': 'Test Announcement',
            'email': 'test@example.com',
            'description': 'This is a test announcement',
            'start_date': '2025-07-16',
            'end_date': '2025-07-23',
            'chapel': True,
            'praise': False
        }
    
    def test_get_submission_form(self):
        """Test GET request returns the submission form."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
        self.assertIsInstance(response.context['form'], SubmissionForm)
    
    def test_post_valid_submission_without_slides(self):
        """Test POST request with valid data but no slides."""
        response = self.client.post(self.url, data=self.valid_data)
        
        # Should redirect on success
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        
        # Check that submission was created
        self.assertTrue(Submission.objects.filter(title='Test Announcement').exists())
    
    def test_post_invalid_form_data(self):
        """Test POST request with invalid form data."""
        invalid_data = self.valid_data.copy()
        invalid_data['chapel'] = False  # Neither chapel nor praise selected
        
        response = self.client.post(self.url, data=invalid_data)
        
        self.assertEqual(response.status_code, 200)  # Should re-render form
        self.assertContains(response, "At least one of &#x27;chapel&#x27; or &#x27;praise&#x27; must be selected.")
    
    def test_post_with_valid_image_slides(self):
        """Test POST request with valid image slides."""
        # Create valid 16:9 images
        image1 = self._create_test_image(1920, 1080, 'test1.png')
        image2 = self._create_test_image(1600, 900, 'test2.jpg')
        
        data = self.valid_data.copy()
        files = {'slides': [image1, image2]}
        
        response = self.client.post(self.url, data=data, files=files)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        
        # Check that submission and slides were created
        submission = Submission.objects.get(title='Test Announcement')
        self.assertEqual(submission.slides.count(), 2)
    
    def test_post_with_invalid_aspect_ratio_slides(self):
        """Test POST request with slides having invalid aspect ratio."""
        # Create image with wrong aspect ratio (4:3 instead of 16:9)
        image = self._create_test_image(1200, 900, 'test.png')
        
        data = self.valid_data.copy()
        files = {'slides': [image]}
        
        response = self.client.post(self.url, data=data, files=files)
        
        self.assertEqual(response.status_code, 200)  # Should re-render form with errors
        self.assertContains(response, "Slide must have a 16:9 aspect ratio")
        
        # Check that no submission was created
        self.assertFalse(Submission.objects.filter(title='Test Announcement').exists())
    
    def test_post_with_invalid_file_extension(self):
        """Test POST request with slides having invalid file extensions."""
        # Create a text file instead of an image
        text_file = SimpleUploadedFile(
            name='test.txt',
            content=b'This is not an image',
            content_type='text/plain'
        )
        
        data = self.valid_data.copy()
        files = {'slides': [text_file]}
        
        response = self.client.post(self.url, data=data, files=files)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Slide must be a PNG or JPG image")
        
        # Check that no submission was created
        self.assertFalse(Submission.objects.filter(title='Test Announcement').exists())
    
    def test_post_with_corrupted_image(self):
        """Test POST request with corrupted image file."""
        corrupted_image = SimpleUploadedFile(
            name='corrupted.png',
            content=b'This is not a valid image file',
            content_type='image/png'
        )
        
        data = self.valid_data.copy()
        files = {'slides': [corrupted_image]}
        
        response = self.client.post(self.url, data=data, files=files)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Uploaded file is not a valid image")
        
        # Check that no submission was created
        self.assertFalse(Submission.objects.filter(title='Test Announcement').exists())
    
    def test_email_sent_for_chapel_announcement(self):
        """Test that email is sent to chapel recipient."""
        data = self.valid_data.copy()
        data['chapel'] = True
        data['praise'] = False
        
        response = self.client.post(self.url, data=data)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'New Announcement')
        self.assertIn('ojthecat127@gmail.com', email.to)
        self.assertIn('Test Announcement', email.body)
    
    def test_email_sent_for_praise_announcement(self):
        """Test that email is sent to praise recipient."""
        data = self.valid_data.copy()
        data['chapel'] = False
        data['praise'] = True
        
        response = self.client.post(self.url, data=data)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'New Announcement')
        self.assertIn('reagan.zierke@student.cune.edu', email.to)
    
    def test_email_sent_for_both_chapel_and_praise(self):
        """Test that email is sent to both recipients when both are selected."""
        data = self.valid_data.copy()
        data['chapel'] = True
        data['praise'] = True
        
        response = self.client.post(self.url, data=data)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        
        email = mail.outbox[0]
        self.assertIn('ojthecat127@gmail.com', email.to)
        self.assertIn('reagan.zierke@student.cune.edu', email.to)
    
    def test_email_attachments_included(self):
        """Test that slide images are attached to emails."""
        image = self._create_test_image(1920, 1080, 'test.png')
        
        data = self.valid_data.copy()
        files = {'slides': [image]}
        
        response = self.client.post(self.url, data=data, files=files)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        
        email = mail.outbox[0]
        self.assertEqual(len(email.attachments), 1)
        self.assertEqual(email.attachments[0][0], 'test.png') 
    
    def _create_test_image(self, width, height, name):
        """Helper method to create a test image file."""
        image = Image.new('RGB', (width, height), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='PNG')
        image_io.seek(0)
        
        return SimpleUploadedFile(
            name=name,
            content=image_io.getvalue(),
            content_type='image/png'
        )


