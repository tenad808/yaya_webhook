from .models import WebhookTransaction
import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
from .utils import verify_yaya_signature, extract_signature_components

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(require_POST, name='dispatch')
class YayaWebhookView(View):
    def post(self, request):
        try:
            # Parse JSON payload
            payload = json.loads(request.body.decode('utf-8'))
            
            # Extract signature from header
            signature_header = request.headers.get('YAYA-SIGNATURE', '')
            if not signature_header:
                logger.warning("Missing YAYA-SIGNATURE header")
                return JsonResponse({'error': 'Missing signature'}, status=400)
            
            # Extract timestamp and signature from header
            timestamp, received_signature = extract_signature_components(signature_header)
            if not timestamp or not received_signature:
                logger.warning("Invalid YAYA-SIGNATURE header format")
                return JsonResponse({'error': 'Invalid signature format'}, status=400)
            
            # Verify signature
            is_valid, message = verify_yaya_signature(
                payload, 
                received_signature, 
                timestamp,
                settings.WEBHOOK_SECRET,
                settings.WEBHOOK_TOLERANCE
            )
            
            if not is_valid:
                logger.warning(f"Signature verification failed: {message}")
                return JsonResponse({'error': message}, status=403)
            
            # Check for replay attacks by verifying transaction hasn't been processed
            yaya_id = payload.get('id')
            if yaya_id and WebhookTransaction.objects.filter(yaya_id=yaya_id).exists():
                logger.warning(f"Possible replay attack detected for transaction {yaya_id}")
                return JsonResponse({'error': 'Transaction already processed'}, status=409)
            
            # Store the transaction
            transaction = WebhookTransaction.objects.create(
                yaya_id=yaya_id,
                amount=payload.get('amount'),
                currency=payload.get('currency'),
                created_at_time=payload.get('created_at_time'),
                timestamp=payload.get('timestamp'),
                cause=payload.get('cause'),
                full_name=payload.get('full_name'),
                account_name=payload.get('account_name'),
                invoice_url=payload.get('invoice_url'),
                signature=received_signature,
                status='pending'  # or 'processed' 
            )
            
            # Process the webhook event
            self.process_webhook_event(payload)
            
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id}, status=200)
            
        except json.JSONDecodeError:
            logger.error("Invalid JSON payload")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    
    def process_webhook_event(self, payload):
        try:
            # Extract and process transaction details
            transaction_data = {
                'transaction_id': payload.get('id'),
                'amount': payload.get('amount'),
                'currency': payload.get('currency'),
                'created_at': payload.get('created_at_time'),
                'timestamp': payload.get('timestamp'),
                'description': payload.get('cause'),
                'customer_name': payload.get('full_name'),
                'account_name': payload.get('account_name'),
                'invoice_url': payload.get('invoice_url')
            }
            logger.info(f"Received valid transaction: {transaction_data}")

        except Exception as e:
            logger.error(f"Error processing webhook event: {str(e)}")