"""
Background tasks and async operations for Sentry testing.
"""
import sentry_sdk
import time
import random
import threading
from datetime import datetime, timedelta

from .config import Config
from .exceptions import ExternalAPIError

def send_email_async(email, subject, body):
    """Send email asynchronously with potential failures."""
    try:
        # Simulate email sending
        if random.random() < 0.15:  # 15% chance of failure
            raise ExternalAPIError("Email service temporarily unavailable")
        
        # Simulate processing time
        time.sleep(random.uniform(1, 3))
        
        return {
            'email': email,
            'subject': subject,
            'status': 'sent',
            'sent_at': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise

def cleanup_old_data(data_type, older_than_days=30):
    """Clean up old data asynchronously."""
    try:
        # Simulate cleanup process
        if random.random() < 0.1:  # 10% chance of failure
            raise Exception("Cleanup service error")
        
        # Simulate processing time
        time.sleep(random.uniform(2, 5))
        
        return {
            'data_type': data_type,
            'records_cleaned': random.randint(100, 5000),
            'status': 'completed',
            'cleaned_at': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise

def process_large_dataset(dataset_id):
    """Process large dataset asynchronously."""
    try:
        # Simulate large dataset processing
        if random.random() < 0.05:  # 5% chance of failure
            raise Exception("Dataset processing service error")
        
        # Simulate long processing time
        time.sleep(random.uniform(5, 15))
        
        return {
            'dataset_id': dataset_id,
            'records_processed': random.randint(10000, 100000),
            'status': 'completed',
            'processed_at': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise

def generate_report_async(report_type, data_filters):
    """Generate report asynchronously."""
    try:
        # Simulate report generation
        if random.random() < 0.08:  # 8% chance of failure
            raise Exception("Report generation service error")
        
        # Simulate processing time
        time.sleep(random.uniform(3, 8))
        
        return {
            'report_type': report_type,
            'filters': data_filters,
            'report_id': f"report_{random.randint(100000, 999999)}",
            'status': 'completed',
            'generated_at': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise

def sync_external_data(sync_type):
    """Sync data with external systems asynchronously."""
    try:
        # Simulate external sync
        if random.random() < 0.12:  # 12% chance of failure
            raise ExternalAPIError("External sync service error")
        
        # Simulate sync time
        time.sleep(random.uniform(2, 6))
        
        return {
            'sync_type': sync_type,
            'records_synced': random.randint(500, 5000),
            'status': 'completed',
            'synced_at': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise

def run_background_task(task_name, *args, **kwargs):
    """Run a background task with error handling."""
    try:
        if task_name == "send_email":
            return send_email_async(*args, **kwargs)
        elif task_name == "cleanup_data":
            return cleanup_old_data(*args, **kwargs)
        elif task_name == "process_dataset":
            return process_large_dataset(*args, **kwargs)
        elif task_name == "generate_report":
            return generate_report_async(*args, **kwargs)
        elif task_name == "sync_data":
            return sync_external_data(*args, **kwargs)
        else:
            raise ValueError(f"Unknown task: {task_name}")
            
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise

class BackgroundTaskManager:
    """Manager for background tasks with error handling."""
    
    def __init__(self):
        self.active_tasks = {}
    
    def start_task(self, task_name, *args, **kwargs):
        """Start a background task."""
        try:
            task_id = f"task_{random.randint(100000, 999999)}"
            self.active_tasks[task_id] = {
                'task_name': task_name,
                'started_at': datetime.utcnow(),
                'status': 'pending'
            }
            
            # Run task in a separate thread
            def run_task():
                try:
                    result = run_background_task(task_name, *args, **kwargs)
                    self.active_tasks[task_id]['status'] = 'completed'
                    self.active_tasks[task_id]['result'] = result
                except Exception as e:
                    self.active_tasks[task_id]['status'] = 'failed'
                    self.active_tasks[task_id]['error'] = str(e)
            
            thread = threading.Thread(target=run_task)
            thread.start()
            
            return task_id
            
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise
    
    def get_task_status(self, task_id):
        """Get the status of a task."""
        try:
            if task_id not in self.active_tasks:
                raise ValueError(f"Task {task_id} not found")
            
            task_info = self.active_tasks[task_id]
            
            return {
                'task_id': task_id,
                'status': task_info['status'],
                'result': task_info.get('result'),
                'error': task_info.get('error')
            }
            
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise
    
    def cancel_task(self, task_id):
        """Cancel a running task."""
        try:
            if task_id not in self.active_tasks:
                raise ValueError(f"Task {task_id} not found")
            
            self.active_tasks[task_id]['status'] = 'cancelled'
            
            return {'task_id': task_id, 'status': 'cancelled'}
            
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise
    
    def cleanup_completed_tasks(self):
        """Clean up completed tasks from memory."""
        try:
            completed_tasks = []
            for task_id, task_info in self.active_tasks.items():
                if task_info['status'] in ['completed', 'failed', 'cancelled']:
                    completed_tasks.append(task_id)
            
            for task_id in completed_tasks:
                del self.active_tasks[task_id]
            
            return {'cleaned_tasks': len(completed_tasks)}
            
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise

# Global task manager instance
task_manager = BackgroundTaskManager()