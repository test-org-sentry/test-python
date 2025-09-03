"""
External API calls that can fail for Sentry testing.
"""
import sentry_sdk
import requests
import time
import random
from requests.exceptions import RequestException, Timeout, ConnectionError, HTTPError

from .config import Config
from .exceptions import ExternalAPIError, PaymentError

def call_external_api(endpoint, timeout=5):
    """Call external API with potential failures."""
    url = f"{Config.EXTERNAL_API_BASE_URL}{endpoint}"
    
    try:
        # Simulate random network issues
        if random.random() < 0.1:  # 10% chance of timeout
            time.sleep(timeout + 1)
        
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        
        return response.json()
        
    except Timeout:
        error_msg = f"API request to {url} timed out after {timeout} seconds"
        sentry_sdk.capture_message(error_msg, level='error')
        raise ExternalAPIError(error_msg)
        
    except ConnectionError:
        error_msg = f"Failed to connect to {url}"
        sentry_sdk.capture_message(error_msg, level='error')
        raise ExternalAPIError(error_msg)
        
    except HTTPError as e:
        error_msg = f"HTTP error {e.response.status_code} from {url}"
        sentry_sdk.capture_exception(e)
        raise ExternalAPIError(error_msg)
        
    except RequestException as e:
        error_msg = f"Request failed for {url}: {str(e)}"
        sentry_sdk.capture_exception(e)
        raise ExternalAPIError(error_msg)

def process_payment(card_number, amount):
    """Process payment with potential failures."""
    try:
        # Simulate payment processing
        if not card_number or len(card_number) < 10:
            raise PaymentError("Invalid card number")
        
        if amount <= 0:
            raise PaymentError("Invalid payment amount")
        
        if amount > 10000:
            raise PaymentError("Payment amount exceeds limit")
        
        # Simulate random payment failures
        if random.random() < 0.2:  # 20% chance of failure
            raise PaymentError("Payment gateway temporarily unavailable")
        
        # Simulate processing time
        time.sleep(random.uniform(0.5, 2.0))
        
        return {
            'transaction_id': f"txn_{random.randint(100000, 999999)}",
            'amount': amount,
            'status': 'success',
            'timestamp': time.time()
        }
        
    except PaymentError:
        raise
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise PaymentError(f"Payment processing failed: {str(e)}")

def send_notification(user_id, message):
    """Send notification via external service."""
    try:
        # Simulate notification service call
        if random.random() < 0.15:  # 15% chance of failure
            raise ExternalAPIError("Notification service unavailable")
        
        # Simulate API call
        response = requests.post(
            f"{Config.EXTERNAL_API_BASE_URL}/post",
            json={
                'user_id': user_id,
                'message': message,
                'timestamp': time.time()
            },
            timeout=10
        )
        
        if response.status_code != 200:
            raise ExternalAPIError(f"Notification failed with status {response.status_code}")
        
        return {
            'notification_id': f"notif_{random.randint(100000, 999999)}",
            'status': 'sent',
            'timestamp': time.time()
        }
        
    except ExternalAPIError:
        raise
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise ExternalAPIError(f"Notification failed: {str(e)}")

def fetch_weather_data(city):
    """Fetch weather data from external API."""
    try:
        # Simulate weather API call
        if random.random() < 0.1:  # 10% chance of failure
            raise ExternalAPIError("Weather service temporarily unavailable")
        
        # Simulate API call to weather service
        response = requests.get(
            f"{Config.EXTERNAL_API_BASE_URL}/json",
            params={'city': city},
            timeout=5
        )
        
        response.raise_for_status()
        data = response.json()
        
        return {
            'city': city,
            'temperature': random.randint(-10, 35),
            'humidity': random.randint(30, 90),
            'description': random.choice(['sunny', 'cloudy', 'rainy', 'snowy']),
            'timestamp': time.time()
        }
        
    except ExternalAPIError:
        raise
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise ExternalAPIError(f"Weather data fetch failed: {str(e)}")

def upload_file(file_path, file_content):
    """Upload file to external storage service."""
    try:
        # Simulate file upload
        if random.random() < 0.05:  # 5% chance of failure
            raise ExternalAPIError("Storage service quota exceeded")
        
        # Simulate upload time
        time.sleep(random.uniform(1, 3))
        
        return {
            'file_id': f"file_{random.randint(100000, 999999)}",
            'file_path': file_path,
            'size': len(file_content),
            'status': 'uploaded',
            'timestamp': time.time()
        }
        
    except ExternalAPIError:
        raise
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise ExternalAPIError(f"File upload failed: {str(e)}")

def sync_data_with_external_system(data):
    """Sync data with external system."""
    try:
        # Simulate data sync
        if random.random() < 0.08:  # 8% chance of failure
            raise ExternalAPIError("External system sync failed")
        
        # Simulate sync time
        time.sleep(random.uniform(0.5, 2.0))
        
        return {
            'sync_id': f"sync_{random.randint(100000, 999999)}",
            'records_processed': len(data) if isinstance(data, list) else 1,
            'status': 'completed',
            'timestamp': time.time()
        }
        
    except ExternalAPIError:
        raise
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise ExternalAPIError(f"Data sync failed: {str(e)}")
