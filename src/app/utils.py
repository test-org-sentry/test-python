"""
Utility functions with various error conditions for Sentry testing.
"""
import sentry_sdk
import re
import os
import json
import random
from datetime import datetime, timedelta

from .exceptions import ValidationError

def validate_email(email):
    """Validate email format with potential errors."""
    try:
        if not email:
            raise ValidationError("Email cannot be empty")
        
        # Simulate random validation errors
        if random.random() < 0.05:  # 5% chance of error
            raise ValidationError("Email validation service unavailable")
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValidationError("Invalid email format")
        
        return True
        
    except ValidationError:
        raise
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise ValidationError(f"Email validation failed: {str(e)}")

def calculate_discount(price, discount_percent, user_type="regular"):
    """Calculate discount with potential calculation errors."""
    try:
        if price < 0:
            raise ValueError("Price cannot be negative")
        
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Discount percent must be between 0 and 100")
        
        # Simulate random calculation errors
        if random.random() < 0.03:  # 3% chance of error
            raise ValueError("Discount calculation service error")
        
        base_discount = price * (discount_percent / 100)
        
        # Apply user type multiplier
        multipliers = {
            "regular": 1.0,
            "premium": 1.1,
            "vip": 1.2
        }
        
        multiplier = multipliers.get(user_type, 1.0)
        final_discount = base_discount * multiplier
        
        return {
            'original_price': price,
            'discount_percent': discount_percent,
            'discount_amount': final_discount,
            'final_price': price - final_discount,
            'user_type': user_type
        }
        
    except ValueError:
        raise
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise ValueError(f"Discount calculation failed: {str(e)}")

def process_file(file_path):
    """Process file with potential file system errors."""
    try:
        if not file_path:
            raise ValueError("File path cannot be empty")
        
        # Simulate random file system errors
        if random.random() < 0.1:  # 10% chance of error
            raise FileNotFoundError("File system temporarily unavailable")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Simulate file processing
        file_size = os.path.getsize(file_path)
        
        # Simulate processing time based on file size
        processing_time = min(file_size / 1000000, 5)  # Max 5 seconds
        time.sleep(processing_time)
        
        return {
            'file_path': file_path,
            'file_size': file_size,
            'processing_time': processing_time,
            'status': 'processed',
            'timestamp': datetime.utcnow().isoformat()
        }
        
    except (FileNotFoundError, ValueError):
        raise
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise Exception(f"File processing failed: {str(e)}")

def generate_report(data, report_type="summary"):
    """Generate report with potential data processing errors."""
    try:
        if not data:
            raise ValueError("No data provided for report generation")
        
        # Simulate random report generation errors
        if random.random() < 0.07:  # 7% chance of error
            raise ValueError("Report generation service error")
        
        # Simulate report processing
        time.sleep(random.uniform(1, 3))
        
        report_data = {
            'report_type': report_type,
            'data_points': len(data) if isinstance(data, list) else 1,
            'generated_at': datetime.utcnow().isoformat(),
            'summary': {
                'total_records': len(data) if isinstance(data, list) else 1,
                'status': 'completed'
            }
        }
        
        return report_data
        
    except ValueError:
        raise
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise Exception(f"Report generation failed: {str(e)}")

def parse_json_data(json_string):
    """Parse JSON data with potential parsing errors."""
    try:
        if not json_string:
            raise ValueError("JSON string cannot be empty")
        
        # Simulate random parsing errors
        if random.random() < 0.05:  # 5% chance of error
            raise ValueError("JSON parsing service error")
        
        data = json.loads(json_string)
        
        return {
            'parsed_data': data,
            'data_type': type(data).__name__,
            'parsed_at': datetime.utcnow().isoformat()
        }
        
    except json.JSONDecodeError as e:
        sentry_sdk.capture_exception(e)
        raise ValueError(f"Invalid JSON format: {str(e)}")
    except ValueError:
        raise
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise Exception(f"JSON parsing failed: {str(e)}")

def encrypt_data(data, key="default-key"):
    """Encrypt data with potential encryption errors."""
    try:
        if not data:
            raise ValueError("Data cannot be empty")
        
        if not key:
            raise ValueError("Encryption key cannot be empty")
        
        # Simulate random encryption errors
        if random.random() < 0.02:  # 2% chance of error
            raise ValueError("Encryption service error")
        
        # Simple encryption simulation (not real encryption)
        encrypted = f"encrypted_{hash(str(data) + key)}"
        
        return {
            'original_data': data,
            'encrypted_data': encrypted,
            'encryption_key': key[:4] + "..." + key[-4:] if len(key) > 8 else "***",
            'encrypted_at': datetime.utcnow().isoformat()
        }
        
    except ValueError:
        raise
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise Exception(f"Data encryption failed: {str(e)}")

def validate_user_input(input_data, validation_rules):
    """Validate user input with potential validation errors."""
    try:
        if not input_data:
            raise ValidationError("Input data cannot be empty")
        
        if not validation_rules:
            raise ValidationError("Validation rules cannot be empty")
        
        # Simulate random validation errors
        if random.random() < 0.06:  # 6% chance of error
            raise ValidationError("Validation service error")
        
        errors = []
        
        for field, rules in validation_rules.items():
            value = input_data.get(field)
            
            if 'required' in rules and not value:
                errors.append(f"{field} is required")
            
            if 'min_length' in rules and value and len(str(value)) < rules['min_length']:
                errors.append(f"{field} must be at least {rules['min_length']} characters")
            
            if 'max_length' in rules and value and len(str(value)) > rules['max_length']:
                errors.append(f"{field} must be no more than {rules['max_length']} characters")
        
        if errors:
            raise ValidationError(f"Validation failed: {', '.join(errors)}")
        
        return {
            'valid': True,
            'validated_data': input_data,
            'validated_at': datetime.utcnow().isoformat()
        }
        
    except ValidationError:
        raise
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise ValidationError(f"Input validation failed: {str(e)}")

def cleanup_old_data(data_type, older_than_days=30):
    """Clean up old data with potential cleanup errors."""
    try:
        if not data_type:
            raise ValueError("Data type cannot be empty")
        
        if older_than_days < 0:
            raise ValueError("Days must be positive")
        
        # Simulate random cleanup errors
        if random.random() < 0.08:  # 8% chance of error
            raise ValueError("Data cleanup service error")
        
        # Simulate cleanup process
        time.sleep(random.uniform(0.5, 2.0))
        
        cutoff_date = datetime.utcnow() - timedelta(days=older_than_days)
        
        return {
            'data_type': data_type,
            'cutoff_date': cutoff_date.isoformat(),
            'records_cleaned': random.randint(10, 1000),
            'cleanup_status': 'completed',
            'cleaned_at': datetime.utcnow().isoformat()
        }
        
    except ValueError:
        raise
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise Exception(f"Data cleanup failed: {str(e)}")
