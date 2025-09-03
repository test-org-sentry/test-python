# Sentry Test Python Project - Complete Setup & Usage Guide

## 🚀 Quick Start with UV

### Prerequisites
- Python 3.8+ installed
- `uv` package manager installed

### Install UV (if not already installed)
```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

### 1. Install Dependencies
```bash
# Install all dependencies
uv sync

# Or install with dev dependencies
uv sync --extra dev
```

### 2. Create Environment File
```bash
cp .env.example .env
# Edit .env with your configuration (optional - defaults are provided)
```

### 3. Run the Application
```bash
# Using uv to run the application
uv run python run.py

# Or activate the virtual environment and run normally
uv shell
python run.py
```

## 📋 Detailed Usage Guide

### Web Interface Testing

1. **Start the Application**:
   ```bash
   uv run python run.py
   ```

2. **Access the Web Interface**:
   - Open http://localhost:5000 in your browser
   - You'll see a comprehensive test interface with buttons for different error types

3. **Test Different Error Scenarios**:
   - **Basic Error Tests**: Click buttons to trigger Python exceptions
   - **Database Errors**: Test database connection and query failures
   - **External API Errors**: Test API timeouts and HTTP errors
   - **Custom Errors**: Test business logic and validation errors
   - **Performance Tests**: Test slow operations and memory issues
   - **User Operations**: Test CRUD operations with potential errors

### API Testing

The application provides REST API endpoints for programmatic testing:

#### User Management
```bash
# List all users
curl http://localhost:5000/api/v1/users

# Create a new user
curl -X POST http://localhost:5000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "name": "Test User"}'

# Get user by ID
curl http://localhost:5000/api/v1/users/1

# Update user
curl -X PUT http://localhost:5000/api/v1/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name"}'

# Delete user
curl -X DELETE http://localhost:5000/api/v1/users/1
```

#### Payment Processing
```bash
# Process a payment
curl -X POST http://localhost:5000/api/v1/payments \
  -H "Content-Type: application/json" \
  -d '{"card_number": "4111-1111-1111-1111", "amount": 100.00}'
```

#### Notifications
```bash
# Send a notification
curl -X POST http://localhost:5000/api/v1/notifications \
  -H "Content-Type: application/json" \
  -d '{"user_id": "123", "message": "Test notification"}'
```

#### Weather Data
```bash
# Get weather data
curl http://localhost:5000/api/v1/weather/New%20York
```

#### Background Tasks
```bash
# Start a background task
curl -X POST http://localhost:5000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"task_name": "send_email", "args": ["test@example.com", "Subject", "Body"]}'

# Check task status
curl http://localhost:5000/api/v1/tasks/{task_id}

# Cancel a task
curl -X DELETE http://localhost:5000/api/v1/tasks/{task_id}
```

#### Reports
```bash
# Generate a report
curl -X POST http://localhost:5000/api/v1/reports \
  -H "Content-Type: application/json" \
  -d '{"report_type": "user_summary", "filters": {"date_range": "30_days"}}'
```

### Script-Based Testing

#### 1. Error Testing Script
```bash
# Run comprehensive error tests
uv run python scripts/test_errors.py
```

This script tests:
- Basic Python errors (division by zero, KeyError, TypeError)
- Custom business logic errors
- Database errors
- External API errors
- Utility function errors
- Performance issues
- Custom Sentry events

#### 2. Load Testing Script
```bash
# Basic load test
uv run python scripts/load_test.py

# Custom load test with specific parameters
uv run python scripts/load_test.py --threads 10 --errors 20

# Stress test (high error rate for 30 seconds)
uv run python scripts/load_test.py --stress
```

#### 3. Production Simulation
```bash
# Run production simulation for 10 minutes
uv run python scripts/simulate_production.py --duration 10

# Run for 30 minutes
uv run python scripts/simulate_production.py --duration 30
```

## 🔧 Development Workflow

### 1. Setting Up Development Environment
```bash
# Install with dev dependencies
uv sync --extra dev

# Activate the virtual environment
uv shell

# Run linting
uv run black src/ scripts/
uv run flake8 src/ scripts/
uv run mypy src/
```

### 2. Adding New Dependencies
```bash
# Add a new dependency
uv add package-name

# Add a dev dependency
uv add --dev package-name

# Update dependencies
uv lock --upgrade
```

### 3. Running Tests
```bash
# Run pytest
uv run pytest

# Run with coverage
uv run pytest --cov=src/
```

## 📊 Sentry Dashboard Monitoring

### What to Look For

1. **Issues Tab**:
   - Error grouping and frequency
   - Stack traces and context
   - User impact and affected users
   - Error trends over time

2. **Performance Tab**:
   - Transaction monitoring
   - Slow database queries
   - External API call timing
   - Background task performance

3. **Releases Tab**:
   - Deployment tracking
   - Error rates by release
   - Performance regression detection

4. **Alerts Tab**:
   - Error rate spikes
   - Performance degradation
   - Custom alert rules

### Key Metrics to Monitor

- **Error Rate**: Percentage of requests that result in errors
- **Response Time**: P50, P95, P99 response times
- **Throughput**: Requests per second
- **User Impact**: Number of affected users
- **Error Types**: Most common error categories

## 🧪 Testing Scenarios

### 1. Basic Error Testing
- Trigger various Python exceptions
- Test error handling and recovery
- Verify error grouping in Sentry

### 2. Performance Testing
- Monitor slow database queries
- Test memory-intensive operations
- Track external API response times

### 3. Load Testing
- Generate high error volumes
- Test error rate limits
- Monitor system performance under load

### 4. Integration Testing
- Test database connections
- Verify external API integrations
- Test background task processing

### 5. User Experience Testing
- Test user registration flow
- Verify payment processing
- Test notification delivery

## 🔍 Debugging Tips

### 1. Sentry Event Details
- Check the "Breadcrumbs" tab for user actions leading to errors
- Review "Context" tab for additional debugging information
- Use "Tags" to filter and group related errors

### 2. Performance Analysis
- Use "Waterfall" view to identify slow operations
- Check "Database" tab for slow queries
- Review "External" tab for API call performance

### 3. Error Investigation
- Use "Stack Trace" to identify the exact error location
- Check "Local Variables" for debugging context
- Review "Request" tab for HTTP request details

## 🚨 Common Issues & Solutions

### 1. Database Connection Errors
- Ensure PostgreSQL is running
- Check database URL in configuration
- Verify database permissions

### 2. Redis Connection Errors
- Ensure Redis is running
- Check Redis URL in configuration
- Verify Redis permissions

### 3. External API Errors
- Check internet connectivity
- Verify API endpoints are accessible
- Review rate limiting

### 4. Sentry Integration Issues
- Verify DSN is correct
- Check Sentry project settings
- Review error sampling configuration

## 📈 Performance Optimization

### 1. Database Optimization
- Monitor slow queries
- Add database indexes
- Optimize query patterns

### 2. API Optimization
- Implement request caching
- Add connection pooling
- Optimize response times

### 3. Background Task Optimization
- Monitor task queue performance
- Optimize task processing
- Implement task prioritization

## 🔐 Security Considerations

### 1. Environment Variables
- Never commit sensitive data to version control
- Use environment variables for configuration
- Implement proper secret management

### 2. API Security
- Implement rate limiting
- Add authentication and authorization
- Validate input data

### 3. Error Handling
- Avoid exposing sensitive information in errors
- Implement proper error logging
- Use structured error responses

## 📝 Best Practices

### 1. Error Handling
- Use specific exception types
- Provide meaningful error messages
- Implement proper error recovery

### 2. Monitoring
- Set up appropriate alerts
- Monitor key performance indicators
- Regular health checks

### 3. Testing
- Write comprehensive tests
- Test error scenarios
- Monitor test coverage

### 4. Documentation
- Keep documentation up to date
- Document error scenarios
- Provide troubleshooting guides

This comprehensive guide should help you effectively use the Sentry test project for your development and testing efforts!
