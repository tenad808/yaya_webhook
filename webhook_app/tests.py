import json
from django.test import TestCase, Client
from django.urls import reverse
import hmac
import hashlib
import time

class WebhookTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.webhook_url = reverse('yaya_webhook') 
        self.valid_payload = {
            "id": "1dd2854e-3a79-4548-ae36-97e4a18ebf81",
            "amount": 100,
            "currency": "ETB",
            "created_at_time": 1673381836,
            "timestamp": 1701272333,
            "cause": "Testing",
            "full_name": "Abebe Kebede",
            "account_name": "abebekebede1",
            "invoice_url": "https://yayawallet.com/en/invoice/xxxx"
        }
    
    def generate_signature(self, payload, secret, timestamp):
        signed_payload = ''.join(str(value) for value in payload.values())
        return hmac.new(
            secret.encode('utf-8'),
            signed_payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def test_valid_webhook(self):
        timestamp = int(time.time())
        signature = self.generate_signature(
            self.valid_payload, 
            'test-secret', 
            timestamp
        )
        
        with self.settings(WEBHOOK_SECRET='test-secret'):
            response = self.client.post(
                self.webhook_url,
                data=json.dumps(self.valid_payload),
                content_type='application/json',
                HTTP_YAYA_SIGNATURE=f't={timestamp},signature={signature}'
            )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
    
    def test_invalid_signature(self):
        timestamp = int(time.time())
        
        with self.settings(WEBHOOK_SECRET='test-secret'):
            response = self.client.post(
                self.webhook_url,
                data=json.dumps(self.valid_payload),
                content_type='application/json',
                HTTP_YAYA_SIGNATURE=f't={timestamp},signature=invalid-signature'
            )
        
        self.assertEqual(response.status_code, 403)
    
    def test_expired_timestamp(self):
        timestamp = int(time.time()) - 600  # 10 minutes ago
        
        signature = self.generate_signature(
            self.valid_payload, 
            'test-secret', 
            timestamp
        )
        
        with self.settings(WEBHOOK_SECRET='test-secret', WEBHOOK_TOLERANCE=300):
            response = self.client.post(
                self.webhook_url,
                data=json.dumps(self.valid_payload),
                content_type='application/json',
                HTTP_YAYA_SIGNATURE=f't={timestamp},signature={signature}'
            )
        
        self.assertEqual(response.status_code, 403)
    
    def test_missing_signature_header(self):
        response = self.client.post(
            self.webhook_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_invalid_json(self):
        timestamp = int(time.time())
        
        response = self.client.post(
            self.webhook_url,
            data='invalid-json',
            content_type='application/json',
            HTTP_YAYA_SIGNATURE=f't={timestamp},signature=test-signature'
        )
        
        self.assertEqual(response.status_code, 400)



