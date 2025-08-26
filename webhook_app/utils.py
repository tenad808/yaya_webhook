import hmac
import hashlib
import time
import json

def verify_yaya_signature(payload, received_signature, timestamp, secret, tolerance=300):
    """
    Verify the YAYA-SIGNATURE header
    """
    # Check if timestamp is within tolerance
    current_time = int(time.time())
    if abs(current_time - timestamp) > tolerance:
        return False, "Timestamp outside tolerance"
    
    # Recreate the exact signed payload string that was used to generate the signature
    signed_payload = create_signed_payload(payload)
    
    # Generate expected signature
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        signed_payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # Compare signatures using constant-time comparison
    if not hmac.compare_digest(expected_signature, received_signature):
        return False, "Invalid signature"
    
    return True, "Signature verified"

def create_signed_payload(payload):
    
    # Concatenate all values in specific order
    ordered_keys = ['id', 'amount', 'currency', 'created_at_time', 'timestamp', 
                   'cause', 'full_name', 'account_name', 'invoice_url']
    
    signed_payload = ''.join(str(payload.get(key, '')) for key in ordered_keys)

    return signed_payload

def extract_signature_components(signature_header):
    """
    Extract timestamp and signature from YAYA-SIGNATURE header
    Expected format: "t=timestamp,signature=signature_value"
    """
    try:
        components = {}
        for part in signature_header.split(','):
            key, value = part.split('=', 1)
            components[key.strip()] = value.strip()
        
        timestamp = int(components.get('t', 0))
        signature = components.get('signature', '')
        
        return timestamp, signature
    except (ValueError, AttributeError):
        return 0, ''