#!/usr/bin/env python3
"""
Standalone script to test various error scenarios for Sentry.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import sentry_sdk
from app.sentry_config import init_sentry
from app.database import init_db, get_user, create_user
from app.external_apis import call_external_api, process_payment
from app.utils import validate_email, calculate_discount, process_file
from app.exceptions import BusinessLogicError, ValidationError

def test_basic_errors():
    """Test basic Python errors."""
    print("Testing basic errors...")
    
    try:
        # Division by zero
        result = 10 / 0
    except ZeroDivisionError as e:
        sentry_sdk.capture_exception(e)
        print(f"✓ Division by zero error captured: {e}")
    
    try:
        # KeyError
        data = {'name': 'test'}
        value = data['email']
    except KeyError as e:
        sentry_sdk.capture_exception(e)
        print(f"✓ KeyError captured: {e}")
    
    try:
        # TypeError
        result = "string" + 123
    except TypeError as e:
        sentry_sdk.capture_exception(e)
        print(f"✓ TypeError captured: {e}")

def test_custom_errors():
    """Test custom business logic errors."""
    print("\nTesting custom errors...")
    
    try:
        raise BusinessLogicError("Payment amount exceeds daily limit")
    except BusinessLogicError as e:
        sentry_sdk.capture_exception(e)
        print(f"✓ BusinessLogicError captured: {e}")
    
    try:
        raise ValidationError("Invalid email format")
    except ValidationError as e:
        sentry_sdk.capture_exception(e)
        print(f"✓ ValidationError captured: {e}")

def test_database_errors():
    """Test database-related errors."""
    print("\nTesting database errors...")
    
    try:
        # Initialize database
        init_db()
        
        # Try to get non-existent user
        user = get_user("999")
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(f"✓ Database error captured: {e}")

def test_external_api_errors():
    """Test external API errors."""
    print("\nTesting external API errors...")
    
    try:
        # Test API timeout
        result = call_external_api("/delay/10")
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(f"✓ External API error captured: {e}")
    
    try:
        # Test payment processing error
        result = process_payment("invalid-card", 100.00)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(f"✓ Payment processing error captured: {e}")

def test_utility_errors():
    """Test utility function errors."""
    print("\nTesting utility errors...")
    
    try:
        # Test email validation error
        validate_email("invalid-email")
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(f"✓ Email validation error captured: {e}")
    
    try:
        # Test discount calculation error
        calculate_discount(-100, 10)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(f"✓ Discount calculation error captured: {e}")
    
    try:
        # Test file processing error
        process_file("nonexistent-file.txt")
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(f"✓ File processing error captured: {e}")

def test_performance_issues():
    """Test performance-related issues."""
    print("\nTesting performance issues...")
    
    # Test slow operation
    with sentry_sdk.start_transaction(op="test", name="slow_operation"):
        import time
        time.sleep(2)  # Simulate slow operation
        print("✓ Slow operation completed")
    
    # Test memory intensive operation
    with sentry_sdk.start_transaction(op="test", name="memory_intensive"):
        data = []
        for i in range(100000):
            data.append(f"item-{i}")
        print(f"✓ Memory intensive operation completed: {len(data)} items")

def test_custom_events():
    """Test custom Sentry events."""
    print("\nTesting custom events...")
    
    # Test custom message
    sentry_sdk.capture_message("This is a test message", level="info")
    print("✓ Custom message sent")
    
    # Test custom event with context
    with sentry_sdk.configure_scope() as scope:
        scope.set_tag("test_type", "custom_event")
        scope.set_context("test_info", {
            "script_name": "test_errors.py",
            "purpose": "Sentry testing"
        })
        sentry_sdk.capture_message("Custom event with context", level="warning")
    print("✓ Custom event with context sent")

def main():
    """Main function to run all tests."""
    print("Starting Sentry error testing...")
    
    # Initialize Sentry
    init_sentry()
    
    # Run all tests
    test_basic_errors()
    test_custom_errors()
    test_database_errors()
    test_external_api_errors()
    test_utility_errors()
    test_performance_issues()
    test_custom_events()
    
    print("\n✓ All tests completed! Check your Sentry dashboard for events.")

if __name__ == "__main__":
    main()
