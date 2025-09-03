# Sentry Test Python Project

This is a comprehensive test project designed for Sentry development and testing. It includes various types of errors, performance issues, and real-world scenarios that can be used to test Sentry's error tracking and performance monitoring capabilities.

## Project Structure

```
test-python/
├── src/
│   └── app/
│       ├── __init__.py
│       ├── app.py                 # Main Flask application
│       ├── api_endpoints.py       # REST API endpoints
│       ├── background_tasks.py    # Celery background tasks
│       ├── config.py              # Configuration settings
│       ├── database.py            # Database operations
│       ├── exceptions.py          # Custom exceptions
│       ├── external_apis.py       # External API calls
│       ├── sentry_config.py       # Sentry configuration
│       └── utils.py               # Utility functions
├── scripts/
│   ├── test_errors.py             # Error testing script
│   ├── load_test.py               # Load testing script
│   └── simulate_production.py     # Production simulation
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── run.py                         # Application entry point
└── README.md                      # This file
```

## Features

### Error Types
- **Basic Python Errors**: Division by zero, KeyError, TypeError, AttributeError
- **Database Errors**: Connection errors, query errors, constraint violations
- **External API Errors**: Timeouts, HTTP errors, connection failures
- **Custom Business Logic Errors**: Payment failures, validation errors, user not found
- **File System Errors**: File not found, permission errors, processing failures

### Performance Monitoring
- **Slow Database Queries**: Simulated slow operations
- **Memory Intensive Operations**: Large data processing
- **Background Tasks**: Celery task monitoring
- **External API Calls**: Request/response timing

### Real-world Scenarios
- **User Registration Flow**: Complete user onboarding with error handling
- **Payment Processing**: Credit card processing with various failure modes
- **Data Processing**: Report generation and data analysis
- **Notification System**: Email and push notification handling

## Setup

### Option 1: Using UV (Recommended)
1. **Install UV** (if not already installed):
   ```bash
   # On macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Install Dependencies**:
   ```bash
   uv sync
   ```

3. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration (optional - defaults provided)
   ```

4. **Run the Application**:
   ```bash
   uv run python run.py
   ```

### Option 2: Using Pip
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the Application**:
   ```bash
   python run.py
   ```

### Access the Web Interface
- Main interface: http://localhost:5000
- API endpoints: http://localhost:5000/api/v1/

## Usage

### Web Interface
The main web interface provides buttons to trigger various types of errors:
- Basic error tests (exceptions, division by zero, etc.)
- Database error tests
- External API error tests
- Custom error tests
- Performance tests
- User operations

### API Endpoints
REST API endpoints for programmatic testing:
- `GET /api/v1/users` - List all users
- `POST /api/v1/users` - Create a new user
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user
- `POST /api/v1/payments` - Process payment
- `POST /api/v1/notifications` - Send notification
- `GET /api/v1/weather/{city}` - Get weather data
- `POST /api/v1/reports` - Generate report
- `POST /api/v1/tasks` - Start background task
- `GET /api/v1/tasks/{id}` - Get task status
- `DELETE /api/v1/tasks/{id}` - Cancel task
- `GET /api/v1/health` - Health check

### Testing Scripts

#### Error Testing Script
```bash
# Using UV
uv run python scripts/test_errors.py

# Using pip
python scripts/test_errors.py
```
Tests various error scenarios and sends them to Sentry.

#### Load Testing Script
```bash
# Using UV
uv run python scripts/load_test.py --threads 5 --errors 10

# Using pip
python scripts/load_test.py --threads 5 --errors 10
```
Generates multiple errors concurrently for load testing.

#### Production Simulation
```bash
# Using UV
uv run python scripts/simulate_production.py --duration 10

# Using pip
python scripts/simulate_production.py --duration 10
```
Simulates production-like scenarios for extended periods.

## Sentry Configuration

The project is configured with your Sentry DSN and includes:
- **Error Tracking**: All exceptions are automatically captured
- **Performance Monitoring**: Transaction tracking for slow operations
- **Custom Context**: Additional tags and context for better debugging
- **Release Tracking**: Version information for deployment tracking

## Error Scenarios

### Database Errors
- Connection timeouts
- Query failures
- Constraint violations
- Data integrity issues

### External API Errors
- HTTP 404, 500 errors
- Connection timeouts
- Service unavailable
- Rate limiting

### Business Logic Errors
- Payment processing failures
- Validation errors
- User authentication issues
- Resource not found

### Performance Issues
- Slow database queries
- Memory leaks
- CPU intensive operations
- Network latency

## Customization

### Adding New Error Types
1. Create new exception classes in `src/app/exceptions.py`
2. Add error scenarios in the appropriate module
3. Update the web interface to include new test buttons
4. Add API endpoints if needed

### Modifying Sentry Configuration
Edit `src/app/sentry_config.py` to:
- Change error sampling rates
- Add custom tags and context
- Configure performance monitoring
- Set up release tracking

### Adding New Test Scenarios
1. Create new functions in the appropriate module
2. Add web interface buttons in `src/app/app.py`
3. Create API endpoints in `src/app/api_endpoints.py`
4. Add test scripts in the `scripts/` directory

## Monitoring

Check your Sentry dashboard for:
- **Issues**: Error tracking and grouping
- **Performance**: Transaction monitoring
- **Releases**: Deployment tracking
- **Alerts**: Error rate notifications

## Troubleshooting

### Common Issues
1. **Database Connection**: Ensure PostgreSQL is running and accessible
2. **Redis Connection**: Ensure Redis is running for background tasks
3. **External APIs**: Some tests use httpbin.org which may be rate limited
4. **Port Conflicts**: Change the port in `run.py` if 5000 is occupied

### Debug Mode
Set `DEBUG=True` in your `.env` file for detailed error information.

## Contributing

This project is designed for Sentry development and testing. Feel free to:
- Add new error scenarios
- Improve existing tests
- Add new monitoring capabilities
- Enhance the web interface

## License

This project is for testing purposes and is not intended for production use.
