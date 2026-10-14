from django.test import TestCase

from .models import Customer


class ContactApiTests(TestCase):
    def test_contact_api_accepts_valid_submission(self):
        response = self.client.post(
            '/contact/api/',
            {
                'full_name': 'Test User',
                'email': 'test@example.com',
                'phone_number': '555-123-4567',
                'message': 'Hello from test.',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'ok': True})
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.first().full_name, 'Test User')

    def test_contact_api_rejects_invalid_submission(self):
        response = self.client.post(
            '/contact/api/',
            {
                'full_name': '',
                'email': 'not-an-email',
                'message': '',
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.json())
