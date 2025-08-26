import os
import django
import time 
import hmac
import hashlib
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yaya_webhook.settings')
django.setup()

from django.conf import settings

payload = {
    "id": "1dd2854e-3a79-4548-ae36",
    "amount": 100,
    "currency": "ETB",
    "created_at_time": 1673381836,
    "timestamp": 1701272333,
    "cause": "Testing Payment",
    "full_name": "Abebe Kebede",
    "account_name": "abebekebede1",
    "invoice_url": "https://yayawallet.com/en/invoice/xxxx"
}

secret = settings.WEBHOOK_SECRET
current_timestamp = int(time.time())
signed_payload = ''.join(str(value) for value in payload.values())
signature = hmac.new(
    secret.encode('utf-8'),
    signed_payload.encode('utf-8'),
    hashlib.sha256
).hexdigest()

print("=== YA-YA WALLET WEBHOOK TESTING ===")
print(f"URL: POST http://127.0.0.1:8000/webhook/yaya/")
print(f'  YAYA-SIGNATURE: t={current_timestamp},signature={signature}')
print("Payload:")
print(payload)




# ===================== Postman Settings on Power Shell or Visual Studio Code Terminal =================
# python manage.py shell -c "
# import hmac
# import hashlib
# import time
# import json
# from django.conf import settings

# # Test payload
# payload = {
#     'id': 'test-' + str(int(time.time())),
#     'amount': 100,
#     'currency': 'ETB',
#     'created_at_time': 1673381836,
#     'timestamp': 1701272333,
#     'cause': 'Test Payment',
#     'full_name': 'Test User',
#     'account_name': 'testuser',
#     'invoice_url': 'https://yayawallet.com/en/invoice/test'
# }

# # Get webhook secret and current timestamp
# secret = settings.WEBHOOK_SECRET
# current_timestamp = int(time.time())

# # Generate signature
# signed_payload = ''.join(str(value) for value in payload.values())
# signature = hmac.new(
#     secret.encode('utf-8'),
#     signed_payload.encode('utf-8'),
#     hashlib.sha256
# ).hexdigest()

# print('=== POSTMAN SETTINGS ===')
# print('URL: POST http://127.0.0.1:8000/webhook/yaya/')
# print('Headers:')
# print('  Content-Type: application/json')
# print(f'  YAYA-SIGNATURE: t={current_timestamp},signature={signature}')
# print('Body (raw JSON):')
# print(json.dumps(payload, indent=2))
# "



