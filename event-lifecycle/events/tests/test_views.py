from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image

from events.models import Event, Participant


def photo_file():
    buf = BytesIO()
    Image.new('RGB', (20, 20), 'white').save(buf, format='JPEG')
    return SimpleUploadedFile('photo.jpg', buf.getvalue(), content_type='image/jpeg')


class ViewTests(TestCase):
    def setUp(self):
        self.event = Event.objects.create(title='Test Event', event_date='2026-10-01')
        self.participant = Participant.objects.create(
            event=self.event,
            name='Test User',
            email='test@example.com',
            transaction_id='TX-500',
            receipt=SimpleUploadedFile('receipt.pdf', b'pdf', content_type='application/pdf'),
            photo=photo_file(),
        )

    def test_dashboard_loads(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')

    def test_stats_endpoint(self):
        response = self.client.get(reverse('dashboard_stats'))
        self.assertEqual(response.json(), {'participants': 1, 'events': 1, 'attended': 0, 'feedback': 0})

    def test_attendance_toggle_requires_ajax(self):
        url = reverse('toggle_attendance', args=[self.participant.pk])
        self.assertEqual(self.client.post(url).status_code, 400)
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.participant.refresh_from_db()
        self.assertTrue(self.participant.attendance)

    def test_marks_update(self):
        response = self.client.post(reverse('update_marks', args=[self.participant.pk]), {'marks': 90})
        self.assertEqual(response.status_code, 200)
        self.participant.refresh_from_db()
        self.assertEqual(self.participant.marks, 90)

    def test_certificate_is_forbidden_until_eligible(self):
        response = self.client.get(reverse('certificate', args=[self.participant.certificate_hash]))
        self.assertEqual(response.status_code, 403)
        self.participant.attendance = True
        self.participant.feedback_given = True
        self.participant.marks = 90
        self.participant.save()
        response = self.client.get(reverse('certificate', args=[self.participant.certificate_hash]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
