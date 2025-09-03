#!/usr/bin/env python3
"""
Script to simulate production-like scenarios for Sentry testing.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import sentry_sdk
import time
import random
import json
from datetime import datetime, timedelta

from app.sentry_config import init_sentry
from app.database import init_db, get_user, create_user, get_all_users
from app.external_apis import call_external_api, process_payment, send_notification
from app.utils import validate_email, calculate_discount, generate_report
from app.exceptions import BusinessLogicError, ValidationError, UserNotFoundError

def simulate_user_registration():
    """Simulate user registration flow with potential errors."""
    print("Simulating user registration...")
    
    # Simulate user registration
    try:
        email = f"user{random.randint(1000, 9999)}@example.com"
        name = f"User {random.randint(1000, 9999)}"
        
        # Validate email
        if not validate_email(email):
            raise ValidationError("Invalid email format")
        
        # Create user
        user = create_user(email, name)
        
        # Send welcome notification
        send_notification(user['id'], f"Welcome {name}!")
        
        print(f"✓ User registered successfully: {email}")
        return user
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(f"✗ User registration failed: {e}")
        return None

def simulate_payment_processing():
    """Simulate payment processing flow."""
    print("Simulating payment processing...")
    
    try:
        # Simulate payment data
        card_number = f"4111-1111-1111-{random.randint(1000, 9999)}"
        amount = random.uniform(10.0, 500.0)
        
        # Process payment
        result = process_payment(card_number, amount)
        
        print(f"✓ Payment processed successfully: ${amount:.2f}")
        return result
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(f"✗ Payment processing failed: {e}")
        return None

def simulate_data_processing():
    """Simulate data processing operations."""
    print("Simulating data processing...")
    
    try:
        # Simulate processing user data
        users = get_all_users()
        
        # Generate report
        report_data = {
            'total_users': len(users),
            'date_range': {
                'start': (datetime.utcnow() - timedelta(days=30)).isoformat(),
                'end': datetime.utcnow().isoformat()
            }
        }
        
        report = generate_report(report_data, "user_summary")
        
        print(f"✓ Data processing completed: {len(users)} users processed")
        return report
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(f"✗ Data processing failed: {e}")
        return None

def simulate_external_api_calls():
    """Simulate external API interactions."""
    print("Simulating external API calls...")
    
    try:
        # Simulate weather data fetch
        cities = ["New York", "London", "Tokyo", "Paris", "Sydney"]
        city = random.choice(cities)
        
        weather_data = call_external_api(f"/json?city={city}")
        
        print(f"✓ Weather data fetched for {city}")
        return weather_data
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(f"✗ External API call failed: {e}")
        return None

def simulate_business_logic_errors():
    """Simulate business logic errors."""
    print("Simulating business logic errors...")
    
    try:
        # Simulate discount calculation
        price = random.uniform(50.0, 1000.0)
        discount = random.uniform(5.0, 25.0)
        user_type = random.choice(["regular", "premium", "vip"])
        
        result = calculate_discount(price, discount, user_type)
        
        print(f"✓ Discount calculated: {discount}% off ${price:.2f}")
        return result
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(f"✗ Business logic error: {e}")
        return None

def simulate_database_operations():
    """Simulate database operations."""
    print("Simulating database operations...")
    
    try:
        # Simulate user lookup
        user_id = random.randint(1, 10)
        user = get_user(str(user_id))
        
        print(f"✓ User retrieved: {user['name']}")
        return user
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(f"✗ Database operation failed: {e}")
        return None

def simulate_performance_issues():
    """Simulate performance-related issues."""
    print("Simulating performance issues...")
    
    # Simulate slow operation
    with sentry_sdk.start_transaction(op="simulation", name="slow_operation"):
        time.sleep(random.uniform(1, 3))
        print("✓ Slow operation completed")
    
    # Simulate memory intensive operation
    with sentry_sdk.start_transaction(op="simulation", name="memory_intensive"):
        data = []
        for i in range(random.randint(50000, 200000)):
            data.append(f"item-{i}")
        print(f"✓ Memory intensive operation completed: {len(data)} items")

def simulate_error_scenarios():
    """Simulate various error scenarios."""
    print("Simulating error scenarios...")
    
    error_scenarios = [
        lambda: 10 / 0,  # Division by zero
        lambda: {'key': 'value'}['missing_key'],  # KeyError
        lambda: "string" + 123,  # TypeError
        lambda: validate_email("invalid-email"),  # Validation error
        lambda: process_payment("invalid-card", 100.00),  # Payment error
        lambda: call_external_api("/status/500"),  # External API error
    ]
    
    for i, scenario in enumerate(error_scenarios):
        try:
            scenario()
        except Exception as e:
            sentry_sdk.capture_exception(e)
            print(f"✓ Error scenario {i+1} triggered: {type(e).__name__}")

def run_production_simulation(duration_minutes=5):
    """Run production-like simulation for specified duration."""
    print(f"Starting production simulation for {duration_minutes} minutes...")
    
    # Initialize Sentry and database
    init_sentry()
    init_db()
    
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)
    
    operation_count = 0
    error_count = 0
    
    while time.time() < end_time:
        try:
            # Randomly choose an operation
            operations = [
                simulate_user_registration,
                simulate_payment_processing,
                simulate_data_processing,
                simulate_external_api_calls,
                simulate_business_logic_errors,
                simulate_database_operations,
                simulate_performance_issues,
            ]
            
            operation = random.choice(operations)
            result = operation()
            
            if result is None:
                error_count += 1
            
            operation_count += 1
            
            # Random delay between operations
            time.sleep(random.uniform(0.5, 2.0))
            
        except KeyboardInterrupt:
            print("\nSimulation interrupted by user")
            break
        except Exception as e:
            sentry_sdk.capture_exception(e)
            error_count += 1
            operation_count += 1
            print(f"✗ Unexpected error: {e}")
    
    duration = time.time() - start_time
    print(f"\nSimulation completed in {duration:.2f} seconds")
    print(f"Total operations: {operation_count}")
    print(f"Errors: {error_count}")
    print(f"Success rate: {((operation_count - error_count) / operation_count * 100):.1f}%")
    
    # Run error scenarios at the end
    simulate_error_scenarios()

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Production simulation script for Sentry")
    parser.add_argument("--duration", type=int, default=5, help="Duration in minutes")
    
    args = parser.parse_args()
    
    run_production_simulation(args.duration)

if __name__ == "__main__":
    main()
