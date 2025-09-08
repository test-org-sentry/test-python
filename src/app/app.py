"""
Main Flask application with various error scenarios for Sentry testing.
"""
import sentry_sdk
from flask import Flask, jsonify, request, render_template_string
import random
import time
import json
from datetime import datetime

from .sentry_config import init_sentry
from .config import Config
from .database import init_db, get_user, create_user, get_all_users
from .external_apis import call_external_api, process_payment
from .utils import validate_email, calculate_discount, process_file
from .background_tasks import send_email_async, cleanup_old_data

def get_sentry_status():
    """Get Sentry configuration status information."""
    return {
        'sentry_dsn_present': bool(Config.SENTRY_DSN),
        'sentry_dsn': Config.SENTRY_DSN,
        'debug_mode': Config.DEBUG,
        'environment': Config.DEBUG and "development" or "production"
    }

# Initialize Sentry
init_sentry()

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
init_db()

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Sentry Test Application</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .button { padding: 10px 20px; margin: 10px; background: #007cba; color: white; border: none; cursor: pointer; }
        .button:hover { background: #005a87; }
        .error { color: red; }
        .success { color: green; }
        .section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; }
        .status-section { margin: 20px 0; padding: 20px; border: 2px solid #007cba; background: #f8f9fa; }
        .status-item { margin: 5px 0; }
        .status-label { font-weight: bold; }
        .status-value { margin-left: 10px; }
        .status-ok { color: #28a745; }
        .status-warning { color: #ffc107; }
        .status-error { color: #dc3545; }
    </style>
</head>
<body>
    <h1>Sentry Test Application</h1>
    <p>This application is designed to generate various types of errors for Sentry testing.</p>
    
    <div class="status-section">
        <h2>🔧 Sentry Configuration Status</h2>
        <div class="status-item">
            <span class="status-label">DSN Present:</span>
            <span class="status-value {{ 'status-ok' if sentry_status.sentry_dsn_present else 'status-error' }}">
                {{ '✅ Yes' if sentry_status.sentry_dsn_present else '❌ No' }}
            </span>
        </div>
        <div class="status-item">
            <span class="status-label">Environment:</span>
            <span class="status-value status-ok">{{ sentry_status.environment.title() }}</span>
        </div>
        <div class="status-item">
            <span class="status-label">Debug Mode:</span>
            <span class="status-value {{ 'status-warning' if sentry_status.debug_mode else 'status-ok' }}">
                {{ '⚠️ Enabled' if sentry_status.debug_mode else '✅ Disabled' }}
            </span>
        </div>
        {% if sentry_status.sentry_dsn %}
        <div class="status-item">
            <span class="status-label">DSN:</span>
            <span class="status-value" style="font-family: monospace; font-size: 0.9em;">{{ sentry_status.sentry_dsn }}</span>
        </div>
        {% endif %}
        {% if not sentry_status.sentry_dsn_present %}
        <div class="status-item" style="margin-top: 15px; padding: 10px; background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 4px;">
            <strong>⚠️ Warning:</strong> Sentry is not configured. Errors will not be sent to Sentry. 
            Please set the SENTRY_DSN environment variable or add it to your .env file.
        </div>
        {% endif %}
    </div>
    
    <div class="section">
        <h2>Basic Error Tests</h2>
        <button class="button" onclick="testError('/test/exception')">Test Exception</button>
        <button class="button" onclick="testError('/test/division-by-zero')">Division by Zero</button>
        <button class="button" onclick="testError('/test/key-error')">Key Error</button>
        <button class="button" onclick="testError('/test/type-error')">Type Error</button>
        <button class="button" onclick="testError('/test/attribute-error')">Attribute Error</button>
    </div>
    
    <div class="section">
        <h2>Database Errors</h2>
        <button class="button" onclick="testError('/test/db-connection')">DB Connection Error</button>
        <button class="button" onclick="testError('/test/db-query')">DB Query Error</button>
        <button class="button" onclick="testError('/test/db-constraint')">DB Constraint Error</button>
    </div>
    
    <div class="section">
        <h2>External API Errors</h2>
        <button class="button" onclick="testError('/test/api-timeout')">API Timeout</button>
        <button class="button" onclick="testError('/test/api-404')">API 404 Error</button>
        <button class="button" onclick="testError('/test/api-500')">API 500 Error</button>
        <button class="button" onclick="testError('/test/payment-failure')">Payment Failure</button>
    </div>
    
    <div class="section">
        <h2>Custom Errors</h2>
        <button class="button" onclick="testError('/test/custom-error')">Custom Business Error</button>
        <button class="button" onclick="testError('/test/validation-error')">Validation Error</button>
        <button class="button" onclick="testError('/test/file-processing')">File Processing Error</button>
    </div>
    
    <div class="section">
        <h2>Performance Tests</h2>
        <button class="button" onclick="testError('/test/slow-query')">Slow Database Query</button>
        <button class="button" onclick="testError('/test/memory-leak')">Memory Intensive Operation</button>
        <button class="button" onclick="testError('/test/background-task')">Background Task Error</button>
    </div>
    
    <div class="section">
        <h2>User Operations</h2>
        <button class="button" onclick="testError('/users')">List Users</button>
        <button class="button" onclick="testError('/users/create')">Create User</button>
        <button class="button" onclick="testError('/users/999')">Get Non-existent User</button>
    </div>
    
    <div id="result"></div>
    
    <script>
        async function testError(url) {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '<p>Testing...</p>';
            
            try {
                const response = await fetch(url);
                
                // Check if response is JSON
                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('application/json')) {
                    const data = await response.json();
                    
                    if (response.ok) {
                        resultDiv.innerHTML = `<p class="success">Success: ${JSON.stringify(data)}</p>`;
                    } else {
                        resultDiv.innerHTML = `<p class="error">Error: ${JSON.stringify(data)}</p>`;
                    }
                } else {
                    // Handle non-JSON responses (like HTML error pages)
                    const text = await response.text();
                    if (response.ok) {
                        resultDiv.innerHTML = `<p class="success">Success: ${text.substring(0, 200)}...</p>`;
                    } else {
                        resultDiv.innerHTML = `<p class="error">Error (${response.status}): ${text.substring(0, 200)}...</p>`;
                    }
                }
            } catch (error) {
                resultDiv.innerHTML = `<p class="error">Network Error: ${error.message}</p>`;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page with test interface."""
    sentry_status = get_sentry_status()
    return render_template_string(HTML_TEMPLATE, sentry_status=sentry_status)

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

# Basic Error Tests
@app.route('/test/exception')
def test_exception():
    """Test basic exception handling."""
    try:
        raise Exception("This is a test exception for Sentry")
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return jsonify({'error': 'Exception raised', 'message': str(e)}), 500

@app.route('/test/division-by-zero')
def test_division_by_zero():
    """Test division by zero error."""
    try:
        result = 10 / 0
        return jsonify({'result': result})
    except ZeroDivisionError as e:
        sentry_sdk.capture_exception(e)
        return jsonify({'error': 'Division by zero', 'message': str(e)}), 500

@app.route('/test/key-error')
def test_key_error():
    """Test KeyError."""
    try:
        data = {'name': 'test'}
        return jsonify({'email': data['email']})  # KeyError: 'email'
    except KeyError as e:
        sentry_sdk.capture_exception(e)
        return jsonify({'error': 'Key error', 'message': str(e)}), 500

@app.route('/test/type-error')
def test_type_error():
    """Test TypeError."""
    try:
        result = "string" + 123  # TypeError
        return jsonify({'result': result})
    except TypeError as e:
        sentry_sdk.capture_exception(e)
        return jsonify({'error': 'Type error', 'message': str(e)}), 500

@app.route('/test/attribute-error')
def test_attribute_error():
    """Test AttributeError."""
    try:
        data = "string"
        return jsonify({'length': data.length})  # AttributeError: 'str' object has no attribute 'length'
    except AttributeError as e:
        sentry_sdk.capture_exception(e)
        return jsonify({'error': 'Attribute error', 'message': str(e)}), 500

# Database Error Tests
@app.route('/test/db-connection')
def test_db_connection():
    """Test database connection error."""
    # This will fail if database is not available
    users = get_all_users()
    return jsonify({'users': users})

@app.route('/test/db-query')
def test_db_query():
    """Test database query error."""
    # Try to get a user with invalid ID
    user = get_user("invalid-id")
    return jsonify({'user': user})

@app.route('/test/db-constraint')
def test_db_constraint():
    """Test database constraint error."""
    # Try to create user with duplicate email
    user = create_user("test@example.com", "Test User")
    return jsonify({'user': user})

# External API Error Tests
@app.route('/test/api-timeout')
def test_api_timeout():
    """Test external API timeout."""
    result = call_external_api("/delay/10")  # This will timeout
    return jsonify({'result': result})

@app.route('/test/api-404')
def test_api_404():
    """Test external API 404 error."""
    result = call_external_api("/status/404")
    return jsonify({'result': result})

@app.route('/test/api-500')
def test_api_500():
    """Test external API 500 error."""
    result = call_external_api("/status/500")
    return jsonify({'result': result})

@app.route('/test/payment-failure')
def test_payment_failure():
    """Test payment processing failure."""
    result = process_payment("invalid-card", 100.00)
    return jsonify({'result': result})

# Custom Error Tests
@app.route('/test/custom-error')
def test_custom_error():
    """Test custom business logic error."""
    from .exceptions import BusinessLogicError
    raise BusinessLogicError("Payment amount exceeds daily limit")

@app.route('/test/validation-error')
def test_validation_error():
    """Test validation error."""
    email = "invalid-email"
    if not validate_email(email):
        from .exceptions import ValidationError
        raise ValidationError("Invalid email format")
    return jsonify({'email': email})

@app.route('/test/file-processing')
def test_file_processing():
    """Test file processing error."""
    result = process_file("nonexistent-file.txt")
    return jsonify({'result': result})

# Performance Tests
@app.route('/test/slow-query')
def test_slow_query():
    """Test slow database query."""
    time.sleep(5)  # Simulate slow query
    users = get_all_users()
    return jsonify({'users': users, 'query_time': '5 seconds'})

@app.route('/test/memory-leak')
def test_memory_leak():
    """Test memory intensive operation."""
    data = []
    for i in range(1000000):
        data.append(f"item-{i}")
    return jsonify({'items_created': len(data)})

@app.route('/test/background-task')
def test_background_task():
    """Test background task error."""
    send_email_async("test@example.com", "Test Subject", "Test Body")
    return jsonify({'message': 'Background task started'})

# User Operations
@app.route('/users')
def list_users():
    """List all users."""
    users = get_all_users()
    return jsonify({'users': users})

@app.route('/users/create', methods=['POST'])
def create_user_endpoint():
    """Create a new user."""
    data = request.get_json() or {}
    email = data.get('email', 'test@example.com')
    name = data.get('name', 'Test User')
    
    user = create_user(email, name)
    return jsonify({'user': user})

@app.route('/users/<user_id>')
def get_user_endpoint(user_id):
    """Get user by ID."""
    user = get_user(user_id)
    if not user:
        from .exceptions import UserNotFoundError
        raise UserNotFoundError(f"User with ID {user_id} not found")
    return jsonify({'user': user})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found', 'message': str(error)}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error', 'message': str(error)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
