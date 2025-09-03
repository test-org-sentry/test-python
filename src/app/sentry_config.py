"""
Sentry configuration and initialization.
"""
import sentry_sdk

from .config import Config

def init_sentry():
    """Initialize Sentry SDK with appropriate integrations."""
    # Use only Flask integration for now to avoid dependency issues
    integrations = []
    
    try:
        from sentry_sdk.integrations.flask import FlaskIntegration
        integrations.append(FlaskIntegration())
    except (ImportError, Exception):
        pass

    sentry_sdk.init(
        dsn=Config.SENTRY_DSN,
        integrations=integrations,
        # Performance monitoring
        traces_sample_rate=1.0,
        # Session tracking
        send_default_pii=True,
        # Environment
        environment=Config.DEBUG and "development" or "production",
        # Release tracking
        release="test-org-sentry/test-python@1.0.0",
        # Disable local variables to avoid serialization issues
        include_local_variables=False,
        # Custom tags
        before_send=before_send_hook,
    )

def before_send_hook(event, hint):
    """Custom hook to modify events before sending to Sentry."""
    # Add custom tags
    event.setdefault('tags', {})
    event['tags']['component'] = 'test-python'
    event['tags']['test_project'] = 'true'
    
    # Add custom context
    event.setdefault('contexts', {})
    event['contexts']['test_info'] = {
        'purpose': 'Sentry development testing',
        'version': '1.0.0'
    }
    
    return event
