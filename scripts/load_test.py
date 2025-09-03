#!/usr/bin/env python3
"""
Load testing script to generate multiple Sentry events.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import sentry_sdk
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.sentry_config import init_sentry
from app.database import get_user, create_user
from app.external_apis import call_external_api, process_payment
from app.utils import validate_email, calculate_discount
from app.exceptions import BusinessLogicError, ValidationError

def generate_random_error():
    """Generate a random error for testing."""
    error_types = [
        "division_by_zero",
        "key_error",
        "type_error",
        "validation_error",
        "business_logic_error",
        "external_api_error",
        "payment_error"
    ]
    
    error_type = random.choice(error_types)
    
    try:
        if error_type == "division_by_zero":
            result = 10 / 0
        elif error_type == "key_error":
            data = {'name': 'test'}
            value = data['email']
        elif error_type == "type_error":
            result = "string" + 123
        elif error_type == "validation_error":
            validate_email("invalid-email")
        elif error_type == "business_logic_error":
            raise BusinessLogicError("Random business logic error")
        elif error_type == "external_api_error":
            call_external_api("/status/500")
        elif error_type == "payment_error":
            process_payment("invalid-card", 100.00)
            
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return f"Generated {error_type}: {str(e)}"
    
    return f"Generated {error_type}: No error occurred"

def worker_thread(thread_id, num_errors):
    """Worker thread to generate errors."""
    results = []
    
    for i in range(num_errors):
        try:
            # Add some randomness to error generation
            if random.random() < 0.7:  # 70% chance of error
                result = generate_random_error()
                results.append(result)
            else:
                # Sometimes do successful operations
                time.sleep(random.uniform(0.1, 0.5))
                results.append(f"Thread {thread_id}: Successful operation {i}")
            
            # Random delay between operations
            time.sleep(random.uniform(0.1, 1.0))
            
        except Exception as e:
            sentry_sdk.capture_exception(e)
            results.append(f"Thread {thread_id}: Unexpected error: {str(e)}")
    
    return results

def run_load_test(num_threads=5, errors_per_thread=10):
    """Run load test with multiple threads."""
    print(f"Starting load test with {num_threads} threads, {errors_per_thread} errors per thread...")
    
    # Initialize Sentry
    init_sentry()
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit tasks
        futures = []
        for i in range(num_threads):
            future = executor.submit(worker_thread, i, errors_per_thread)
            futures.append(future)
        
        # Collect results
        all_results = []
        for future in as_completed(futures):
            try:
                results = future.result()
                all_results.extend(results)
            except Exception as e:
                sentry_sdk.capture_exception(e)
                print(f"Thread failed: {e}")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\nLoad test completed in {duration:.2f} seconds")
    print(f"Total operations: {len(all_results)}")
    print(f"Operations per second: {len(all_results) / duration:.2f}")
    
    # Count error types
    error_counts = {}
    for result in all_results:
        if "Generated" in result and ":" in result:
            error_type = result.split("Generated ")[1].split(":")[0]
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
    
    print("\nError type distribution:")
    for error_type, count in error_counts.items():
        print(f"  {error_type}: {count}")

def run_stress_test():
    """Run stress test with high error rate."""
    print("Running stress test...")
    
    # Initialize Sentry
    init_sentry()
    
    start_time = time.time()
    error_count = 0
    
    try:
        while time.time() - start_time < 30:  # Run for 30 seconds
            try:
                # Generate errors rapidly
                if random.random() < 0.9:  # 90% error rate
                    generate_random_error()
                    error_count += 1
                
                time.sleep(0.01)  # Very short delay
                
            except Exception as e:
                sentry_sdk.capture_exception(e)
                error_count += 1
    
    except KeyboardInterrupt:
        print("\nStress test interrupted by user")
    
    duration = time.time() - start_time
    print(f"Stress test completed in {duration:.2f} seconds")
    print(f"Total errors generated: {error_count}")
    print(f"Errors per second: {error_count / duration:.2f}")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Load test script for Sentry")
    parser.add_argument("--threads", type=int, default=5, help="Number of threads")
    parser.add_argument("--errors", type=int, default=10, help="Errors per thread")
    parser.add_argument("--stress", action="store_true", help="Run stress test")
    
    args = parser.parse_args()
    
    if args.stress:
        run_stress_test()
    else:
        run_load_test(args.threads, args.errors)

if __name__ == "__main__":
    main()
