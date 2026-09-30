from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from events.models import Event, Participant


class ParticipantModelTests(TestCase):
    def setUp(self):
        self.event = Event.objects.create(title='Django Day', event_date='2026-10-01')
        self.photo = SimpleUploadedFile('photo.jpg', b'fake-image', content_type='image/jpeg')
        self.receipt = SimpleUploadedFile('receipt.pdf', b'pdf', content_type='application/pdf')

    def participant(self, **kwargs):
        data = {
            'event': self.event,
            'name': 'Test User',
            'email': 'test@example.com',
            'transaction_id': 'TX-1',
            'receipt': self.receipt,
            'photo': self.photo,
        }
        data.update(kwargs)
        return Participant.objects.create(**data)

    def test_certificate_requires_all_three_conditions(self):
        p = self.participant()
        self.assertFalse(p.is_eligible())
        p.attendance = True
        p.save()
        self.assertFalse(p.is_eligible())
        p.feedback_given = True
        p.marks = 85
        p.save()
        self.assertTrue(p.is_eligible())

    def test_transaction_id_is_unique(self):
        self.participant()
        with self.assertRaises(Exception):
            self.participant(transaction_id='TX-1', name='Second')
