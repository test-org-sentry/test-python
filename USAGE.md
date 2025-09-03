# Sentry Test Python - Usage Guide

A simple test application for generating various types of errors to test Sentry's error tracking and performance monitoring capabilities.

## Quick Start

### 1. Install Dependencies

**Using UV (Recommended):**
```bash
# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync
```

**Using pip:**
```bash
pip install -r requirements.txt
```

### 2. Run the Application

**Using UV:**
```bash
uv run python run.py
```

**Using pip:**
```bash
python run.py
```

The application will start on http://localhost:5000

### 3. Test with Sentry

#### Web Interface
1. Open http://localhost:5000 in your browser
2. Click any of the test buttons to generate different types of errors:
   - **Basic Error Tests**: Exceptions, division by zero, key errors, type errors
   - **Database Errors**: Connection failures, query errors, constraint violations
   - **External API Errors**: Timeouts, HTTP errors, connection failures
   - **Custom Errors**: Business logic errors, validation errors
   - **Performance Tests**: Slow operations, memory issues

#### API Testing
```bash
# Test basic errors
curl http://localhost:5000/test/exception
curl http://localhost:5000/test/division-by-zero

# Test user operations
curl http://localhost:5000/api/v1/users
curl -X POST http://localhost:5000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "name": "Test User"}'

# Test payments
curl -X POST http://localhost:5000/api/v1/payments \
  -H "Content-Type: application/json" \
  -d '{"card_number": "4111-1111-1111-1111", "amount": 100.00}'
```

#### Script Testing
```bash
# Run comprehensive error tests
uv run python scripts/test_errors.py

# Load test with multiple threads
uv run python scripts/load_test.py --threads 5 --errors 10

# Simulate production scenarios
uv run python scripts/simulate_production.py --duration 10
```

## What You'll See in Sentry

Check your Sentry dashboard for:
- **Issues**: Error tracking with stack traces and context
- **Performance**: Transaction monitoring for slow operations
- **Custom Tags**: `component: test-python`, `test_project: true`
- **Error Types**: Python exceptions, custom business logic errors, API failures

## Configuration

The application is pre-configured with your Sentry DSN. To modify settings:

1. Copy `.env.example` to `.env`
2. Edit the configuration in `src/app/config.py`
3. Restart the application

## Available Endpoints

### Test Endpoints
- `/test/exception` - Basic exception
- `/test/division-by-zero` - Division by zero error
- `/test/key-error` - KeyError
- `/test/type-error` - TypeError
- `/test/attribute-error` - AttributeError
- `/test/db-connection` - Database connection error
- `/test/api-timeout` - External API timeout
- `/test/payment-failure` - Payment processing error

### API Endpoints
- `GET /api/v1/users` - List users
- `POST /api/v1/users` - Create user
- `GET /api/v1/users/{id}` - Get user by ID
- `POST /api/v1/payments` - Process payment
- `POST /api/v1/notifications` - Send notification
- `GET /api/v1/health` - Health check

## Troubleshooting

**Application won't start:**
- Ensure Python 3.8+ is installed
- Check that all dependencies are installed
- Verify port 5000 is available

**No errors in Sentry:**
- Check your Sentry DSN is correct
- Verify network connectivity
- Check Sentry project settings

**Database errors:**
- The application works without a database (uses mock data)
- To use real database: `uv sync --extra database`

## Stopping the Application

Press `Ctrl+C` in the terminal where the application is running.
