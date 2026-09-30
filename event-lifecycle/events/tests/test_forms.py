from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from events.forms import FeedbackForm, MarksForm, RegistrationForm
from events.models import Event


def image_file():
    buf = BytesIO()
    Image.new('RGB', (20, 20), 'white').save(buf, format='JPEG')
    return SimpleUploadedFile('photo.jpg', buf.getvalue(), content_type='image/jpeg')


class FormTests(TestCase):
    def setUp(self):
        self.event = Event.objects.create(title='Test Event', event_date='2026-10-01')

    def registration_data(self, transaction_id='TX-100'):
        return {
            'event': self.event.pk,
            'name': 'Test User',
            'email': 'test@example.com',
            'transaction_id': transaction_id,
            'receipt': SimpleUploadedFile('receipt.pdf', b'pdf', content_type='application/pdf'),
            'photo': image_file(),
        }

    def test_registration_accepts_valid_input(self):
        form = RegistrationForm(data=self.registration_data(), files=self.registration_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_marks_reject_out_of_range(self):
        form = MarksForm(data={'marks': 101})
        self.assertFalse(form.is_valid())

    def test_feedback_rejects_invalid_rating(self):
        form = FeedbackForm(data={'rating': 6, 'comment': 'Too high'})
        self.assertFalse(form.is_valid())
