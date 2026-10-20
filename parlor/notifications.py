import os
import json
import logging
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)


def send_whatsapp_notification(appointment, request=None):
    """
    Automated background WhatsApp dispatch using Python standard library (urllib.request)
    if an external WhatsApp Gateway/API (such as UltraMsg, GreenAPI, Meta Cloud API, etc.)
    is configured in environment variables.
    
    If credentials are not present, it logs gracefully and relies on the client-side & admin portal 1-click trigger.
    """
    api_url = os.environ.get('WHATSAPP_API_URL')
    token = os.environ.get('WHATSAPP_API_TOKEN')

    if not api_url or not token:
        logger.info(f"WHATSAPP_API_URL / TOKEN not set in environment. Client/Portal 1-click WhatsApp trigger active for {appointment.booking_reference}.")
        return False

    phone = appointment.clean_whatsapp_number
    message = appointment.get_whatsapp_confirmation_text(request)

    payload = {
        'token': token,
        'to': phone,
        'body': message
    }
    instance_id = os.environ.get('WHATSAPP_INSTANCE_ID')
    if instance_id:
        payload['instanceId'] = instance_id

    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            api_url, 
            data=data, 
            headers={'Content-Type': 'application/json', 'User-Agent': 'NishiParlour/1.0'}
        )
        with urllib.request.urlopen(req, timeout=6) as response:
            status_code = response.getcode()
            logger.info(f"WhatsApp notification sent for {appointment.booking_reference}, status: {status_code}")
            return 200 <= status_code < 300
    except Exception as e:
        logger.error(f"Error sending WhatsApp notification for {appointment.booking_reference}: {e}")
        return False
