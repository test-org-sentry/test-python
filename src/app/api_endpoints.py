"""
Additional API endpoints for comprehensive Sentry testing.
"""
import sentry_sdk
from flask import Blueprint, jsonify, request
import random
import time
from datetime import datetime

from .database import get_user, create_user, update_user, delete_user, get_all_users
from .external_apis import call_external_api, process_payment, send_notification, fetch_weather_data
from .utils import validate_email, calculate_discount, process_file, generate_report
from .background_tasks import task_manager
from .exceptions import ValidationError, BusinessLogicError, UserNotFoundError

# Create blueprint for additional endpoints
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/users', methods=['GET'])
def api_list_users():
    """API endpoint to list all users."""
    try:
        users = get_all_users()
        return jsonify({
            'success': True,
            'data': users,
            'count': len(users),
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@api_bp.route('/users', methods=['POST'])
def api_create_user():
    """API endpoint to create a new user."""
    try:
        data = request.get_json()
        if not data:
            raise ValidationError("Request body is required")
        
        email = data.get('email')
        name = data.get('name')
        
        if not email or not name:
            raise ValidationError("Email and name are required")
        
        if not validate_email(email):
            raise ValidationError("Invalid email format")
        
        user = create_user(email, name)
        
        return jsonify({
            'success': True,
            'data': user,
            'timestamp': datetime.utcnow().isoformat()
        }), 201
        
    except ValidationError as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 400
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@api_bp.route('/users/<user_id>', methods=['GET'])
def api_get_user(user_id):
    """API endpoint to get a user by ID."""
    try:
        user = get_user(user_id)
        return jsonify({
            'success': True,
            'data': user,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except UserNotFoundError as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 404
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@api_bp.route('/users/<user_id>', methods=['PUT'])
def api_update_user(user_id):
    """API endpoint to update a user."""
    try:
        data = request.get_json()
        if not data:
            raise ValidationError("Request body is required")
        
        user = update_user(user_id, **data)
        
        return jsonify({
            'success': True,
            'data': user,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except UserNotFoundError as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 404
        
    except ValidationError as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 400
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@api_bp.route('/users/<user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    """API endpoint to delete a user."""
    try:
        result = delete_user(user_id)
        return jsonify({
            'success': True,
            'data': result,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except UserNotFoundError as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 404
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@api_bp.route('/payments', methods=['POST'])
def api_process_payment():
    """API endpoint to process payments."""
    try:
        data = request.get_json()
        if not data:
            raise ValidationError("Request body is required")
        
        card_number = data.get('card_number')
        amount = data.get('amount')
        
        if not card_number or not amount:
            raise ValidationError("Card number and amount are required")
        
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValidationError("Amount must be a positive number")
        
        result = process_payment(card_number, amount)
        
        return jsonify({
            'success': True,
            'data': result,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except ValidationError as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 400
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@api_bp.route('/notifications', methods=['POST'])
def api_send_notification():
    """API endpoint to send notifications."""
    try:
        data = request.get_json()
        if not data:
            raise ValidationError("Request body is required")
        
        user_id = data.get('user_id')
        message = data.get('message')
        
        if not user_id or not message:
            raise ValidationError("User ID and message are required")
        
        result = send_notification(user_id, message)
        
        return jsonify({
            'success': True,
            'data': result,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except ValidationError as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 400
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@api_bp.route('/weather/<city>', methods=['GET'])
def api_get_weather(city):
    """API endpoint to get weather data."""
    try:
        if not city:
            raise ValidationError("City name is required")
        
        result = fetch_weather_data(city)
        
        return jsonify({
            'success': True,
            'data': result,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except ValidationError as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 400
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@api_bp.route('/reports', methods=['POST'])
def api_generate_report():
    """API endpoint to generate reports."""
    try:
        data = request.get_json()
        if not data:
            raise ValidationError("Request body is required")
        
        report_type = data.get('report_type', 'summary')
        data_filters = data.get('filters', {})
        
        result = generate_report(data_filters, report_type)
        
        return jsonify({
            'success': True,
            'data': result,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except ValidationError as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 400
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@api_bp.route('/tasks', methods=['POST'])
def api_start_background_task():
    """API endpoint to start background tasks."""
    try:
        data = request.get_json()
        if not data:
            raise ValidationError("Request body is required")
        
        task_name = data.get('task_name')
        task_args = data.get('args', [])
        task_kwargs = data.get('kwargs', {})
        
        if not task_name:
            raise ValidationError("Task name is required")
        
        task_id = task_manager.start_task(task_name, *task_args, **task_kwargs)
        
        return jsonify({
            'success': True,
            'data': {'task_id': task_id},
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except ValidationError as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 400
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@api_bp.route('/tasks/<task_id>', methods=['GET'])
def api_get_task_status(task_id):
    """API endpoint to get task status."""
    try:
        if not task_id:
            raise ValidationError("Task ID is required")
        
        status = task_manager.get_task_status(task_id)
        
        return jsonify({
            'success': True,
            'data': status,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except ValidationError as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 400
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@api_bp.route('/tasks/<task_id>', methods=['DELETE'])
def api_cancel_task(task_id):
    """API endpoint to cancel a task."""
    try:
        if not task_id:
            raise ValidationError("Task ID is required")
        
        result = task_manager.cancel_task(task_id)
        
        return jsonify({
            'success': True,
            'data': result,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except ValidationError as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 400
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@api_bp.route('/health', methods=['GET'])
def api_health_check():
    """API endpoint for health checks."""
    try:
        # Simulate random health check failures
        if random.random() < 0.05:  # 5% chance of failure
            raise Exception("Health check service error")
        
        return jsonify({
            'success': True,
            'data': {
                'status': 'healthy',
                'timestamp': datetime.utcnow().isoformat(),
                'version': '1.0.0',
                'services': {
                    'database': 'healthy',
                    'redis': 'healthy',
                    'external_apis': 'healthy'
                }
            }
        })
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500
