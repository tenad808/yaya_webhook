# YaYa Wallet Webhook Endpoint

A Django-based webhook endpoint for receiving and processing YaYa Wallet transaction notifications.

## Features

- Receives webhook POST requests with JSON payload
- Verifies YAYA-SIGNATURE header for security
- Handles replay attacks with timestamp validation
- Validates payload structure
- Prevents duplicate transaction processing
- Returns 2xx response immediately before processing
- Comprehensive test suite

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/tenad808/yaya_webhook.git
   cd yaya_webhook
Install dependencies

bash
pip install -r requirements.txt
Configure environment variables

bash
cp .env.example .env
# Edit .env with your settings
Run migrations

bash
python manage.py migrate
Start the development server

bash
python manage.py runserver
Testing
Run the test suite:

bash
python manage.py test
Testing Webhook Endpoint
Use curl to test the webhook endpoint:

bash
curl -X POST http://localhost:8000/webhook/yaya/ \
  -H "Content-Type: application/json" \
  -H "YAYA-SIGNATURE: generated_signature_here" \
  -d '{
    "id": "1dd2854e-3a79-4548-ae36-97e4a18ebf81",
    "amount": 100,
    "currency": "ETB",
    "created_at_time": 1673381836,
    "timestamp": 1701272333,
    "cause": "Testing",
    "full_name": "Abebe Kebede",
    "account_name": "abebekebede1",
    "invoice_url": "https://yayawallet.com/en/invoice/xxxx"
  }'
Security Considerations
Webhook secret is stored in environment variables

HMAC SHA256 signature verification

Replay attack protection with 5-minute tolerance window

Input validation and sanitization

Duplicate transaction prevention

Production Deployment
For production deployment:

Set DEBUG=False

Use a proper database (PostgreSQL recommended)

Set up HTTPS

Use a proper web server (nginx + gunicorn)

Implement proper logging and monitoring

Use Celery for asynchronous task processing

Set up proper error handling and alerts

Assumptions
The webhook payload structure matches the provided example

Timestamps are in Unix time format

All currency amounts are represented as numbers

The system clock is synchronized with NTP

Webhook processing can be done asynchronously after responding

API Endpoint
URL: /webhook/yaya/

Method: POST

Headers:

Content-Type: application/json

YAYA-SIGNATURE: <signature>

Response: Immediate 200 response with processing done asynchronously

text

## How to Test

1. **Unit Tests**: Run `python manage.py test` to execute the test suite
2. **Manual Testing**: Use curl or Postman to send test requests
3. **Signature Verification**: Test with valid and invalid signatures
4. **Replay Attack**: Test with old timestamps to verify rejection
5. **Duplicate Handling**: Test sending the same transaction multiple times

## Key Security Features

1. **Signature Verification**: Uses HMAC SHA256 to verify request authenticity
2. **Replay Attack Protection**: Checks timestamp within tolerance window
3. **Input Validation**: Validates all required fields and data types
4. **Duplicate Prevention**: Checks for already processed transactions
5. **Error Handling**: Proper error responses without exposing internal details

This implementation provides a robust, secure webhook endpoint that meets all YaYa Wallet requirements while maintaining code quality and testability.



Found 5 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
Signature verification failed: Timestamp outside tolerance   <-- expected for expired timestamp test
.Invalid JSON payload                                        <-- expected for invalid JSON test
.Signature verification failed: Invalid signature            <-- expected for wrong signature test
.Missing YAYA-SIGNATURE header                               <-- expected for missing header test
..
----------------------------------------------------------------------
Ran 5 tests in 0.015s

OK
Destroying test database for alias 'default'...
