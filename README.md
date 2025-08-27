# YaYa Wallet Webhook Integration
## 📋 Project Overview
This solution implements a secure webhook endpoint for processing YaYa Wallet transaction notifications, following the guidelines provided in the YaYa Wallet documentation. The implementation is built using Django and Python, featuring robust security measures including HMAC signature verification, replay attack protection, and comprehensive error handling.

## 🚀 Features and Solution Works as Expected

- **Secure Webhook Processing**: HMAC-SHA256 signature verification and verifies YAYA-SIGNATURE header for security
- **Replay Attack Protection**: Timestamp tolerance checking and duplicate transaction detection
- **RESTful API**: Clean JSON-based webhook endpoint
- **Quick Response**: Returns 2xx immediately before processing
- **Comprehensive Testing**: Full test suite covering all security scenarios
- **Database Logging**: Stores all webhook transactions for auditing and debugging

## Technical Implementation

#### Problem-Solving Approach
1. Requirements Analysis: Studied YaYa Wallet webhook documentation thoroughly
2. Security First: Prioritized signature verification and replay protection
3. Modular Design: Separated concerns into models, views, utils, and tests
4. Error Handling: Implemented comprehensive validation and error responses
5. Testing: Built complete test suite before final implementation
6. Documentation: Created detailed setup and usage instructions
#### Assumptions Made
1. Timestamp Handling:
      - created_at_time represents original transaction creation 
      - timestamp represents webhook delivery time 
      - 5-minute tolerance window for timestamp validation
2. Security:
      - Webhook secret is stored securely in environment variables
      - HMAC-SHA256 is used for signature verification
      - Constant-time comparison to prevent timing attacks
3. Data Validation:
      - All required fields must be present in payload
      - Numeric fields validated as numbers
      - String fields validated for presence and type
4. Async Processing:
      - Immediate 2xx response returned before processing
      - Background processing happens after response delivery

## 🚀 Quick Start

## 📋 Prerequisites

- Python 3.8+
- Django 5.2.5+
- PostgreSQL (recommended) or SQLite
- python-decouple for environment variable management

## Project Structure
      yaya_webhook/
      ├── manage.py
      ├── requirements.txt
      ├── .env                    # Environment variables (gitignored)
      ├── generate_signature.py   # For manual testing
      ├── yaya_webhook/          # Main project directory
      │   ├── __init__.py
      │   ├── settings.py        # Django settings with webhook config
      │   ├── urls.py           # URL routing
      │   └── wsgi.py
      └── webhook_app/           # Webhook application
          ├── __init__.py
          ├── admin.py          # Django admin configuration
          ├── apps.py           # App configuration
          ├── models.py         # WebhookTransaction model
          ├── tests.py          # Comprehensive test suite
          ├── urls.py          # App URL patterns
          ├── utils.py          # Security utilities
          └── views.py          # Webhook view handlers

## Setup Instructions

1. **Clone the repository**
   ```bash
      git clone https://github.com/tenad808/yaya_webhook.git
      cd yaya_webhook

2. **Install dependencies**
   ```bash
      pip install -r requirements.txt

3. **Configure environment variables**
   ```bash
      cp .env.example .env
      # Edit .env with your settings
      # DEBUG=True
      # DJANGO_SECRET_KEY=your-secure-secret-key-here 
      # WEBHOOK_SECRET=your-yaya-webhook-secret
      # WEBHOOK_TOLERANCE=300
      # ALLOWED_HOSTS=localhost,127.0.0.1
4. **Configure Database**
    ```bash
      # Go to the path yaya_webhook/settings.py
      # For PostgreSQL (recommended):
      DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'yaya_webhook', # or your database name
                'USER': 'postgres',     # or your database username
                'PASSWORD': 'root',     # or your database password
                'HOST': 'localhost',
                'PORT': '5432',
            }
        }
      # Or for SQLite (development):
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

6. **Run migrations**
   ```bash
      python manage.py makemigrations
      python manage.py migrate

7. **Start the development server**
   ```bash
      python manage.py runserver

## Testing

1. **Unit Tests**
   ```bash
      # Run all tests
      python manage.py test

        # Expected test output shows:
        # Found 5 test(s).
        # Creating test database for alias 'default'...
        # System check identified no issues (0 silenced).
        # Signature verification failed: Timestamp outside tolerance   <-- expected for expired timestamp test
        # .Invalid JSON payload                                        <-- expected for invalid JSON test
        # .Signature verification failed: Invalid signature            <-- expected for wrong signature test
        # .Missing YAYA-SIGNATURE header                               <-- expected for missing header test
        # ..
        # ----------------------------------------------------------------------
        # Ran 5 tests in 0.015s

        # OK
        # Destroying test database for alias 'default'...

2. **Manual Testing**
   ```bash
       #Option 1: Using generate_signature.py
       python generate_signature.py
             
       #Option 2: Generate test signature and payload using shell or terminal
         # Run this code on power shell or visual studio terminal on the project path
         python manage.py shell -c "
          import hmac
          import hashlib
          import time
          import json
          from django.conf import settings
          # Test payload
          payload = {
              'id': 'test-' + str(int(time.time())),
              'amount': 100,
              'currency': 'ETB',
              'created_at_time': 1673381836,
              'timestamp': 1701272333,
              'cause': 'Testing  Payment',
              'full_name': 'Abebe Kebede',
              'account_name': 'abebekebede1',
              'invoice_url': 'https://yayawallet.com/en/invoice/xxxx'
          }
      
          # Get webhook secret and current timestamp
          secret = settings.WEBHOOK_SECRET
          current_timestamp = int(time.time())
      
          # Generate signature
          signed_payload = ''.join(str(value) for value in payload.values())
          signature = hmac.new(
              secret.encode('utf-8'),
              signed_payload.encode('utf-8'),
              hashlib.sha256
          ).hexdigest()
      
          print('=== POSTMAN SETTINGS ===')
          print('URL: POST http://127.0.0.1:8000/webhook/yaya/')
          print('Headers:')
          print('  Content-Type: application/json')
          print(f'  YAYA-SIGNATURE: t={current_timestamp},signature={signature}')
          print('Body (raw JSON):')
          print(json.dumps(payload, indent=2))
          "

          
          ###### Expected test output shows:
          # === POSTMAN SETTINGS ===
          # URL: POST http://127.0.0.1:8000/webhook/yaya/   
          # Headers:
            # Content-Type: application/json               
            # YAYA-SIGNATURE: t=1756277039,signature=af80273b564ac21fbfd8c0abe0d33d14d53a1969e16c67a8505f84914f885ff7  
          # Body (raw JSON):       
          # {
            # "id": "test-1756277039",
            # "amount": 100,
            # "currency": "ETB",
            # "created_at_time": 1673381836,
            # "timestamp": 1701272333,
            # "cause": "Testing Payment",
            # "full_name": "Abebe Kebede",
            # "account_name": "abebekebede1",
            # "invoice_url": "https://yayawallet.com/en/invoice/xxxx"
          # }

 4. **Postman Testing Setup**
    **Use the generated output in Postman**
    
    **Request Configuration:** 
       - **Method**: POST
       - **URL**: http://127.0.0.1:8000/webhook/yaya/
    
    **Headers:**
        `Content-Type:` `application/json` and
        `YAYA-SIGNATURE:` `[generated_signature]`
    
    **Body (raw JSON):**
    ```bash
        {
          "id": "test-1234567890",
          "amount": 100,
          "currency": "ETB",
          "created_at_time": 1673381836,
          "timestamp": 1701272333,
          "cause": "Testing Payment",
          "full_name": "Abebe Kebede",
          "account_name": "abebekebede1",
          "invoice_url": "https://yayawallet.com/en/invoice/xxxx"
      }

## API Endpoint
### Webhook URL
    POST /webhook/yaya/
### Request Headers
    Content-Type: application/json
    YAYA-SIGNATURE: t={timestamp},signature={hmac_signature}
### Request Body
    {
        "id": "string (UUID)",
        "amount": "number",
        "currency": "string (3 chars)",
        "created_at_time": "number (timestamp)",
        "timestamp": "number (timestamp)", 
        "cause": "string",
        "full_name": "string",
        "account_name": "string",
        "invoice_url": "string (URL)"
      }
### Response Codes
    200 - Webhook processed successfully
    # {"status": "success"}
    400 - Invalid JSON or missing signature header
    # {"error": "Invalid JSON"} or {"error": "Invalid signature"}
    409 - Duplicate transaction (replay attack detected)
    # {"error": "Transaction already processed"}
## 📝 Implementation Notes
#### Challenges Solved:
1. Signature Verification: Implemented proper HMAC-SHA256 with constant-time comparison
2. Timestamp Handling: Managed both historical and current timestamps appropriately
3. Error Handling: Comprehensive validation without exposing internal details
4. Testing: Covered all edge cases including security scenarios
#### Design Decisions:
1. Django Framework: Chosen for rapid development and security features
2. Modular Structure: Separated concerns for maintainability
3. Environment Configuration: Used python-decouple for secure configuration
4. Testing First: Built comprehensive tests before final implementation
       
