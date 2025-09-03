"""
Database operations with potential errors for Sentry testing.
"""
import sentry_sdk
from datetime import datetime
import random

from .config import Config
from .exceptions import UserNotFoundError

# Try to import SQLAlchemy, fall back to mock if not available
try:
    from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False
    # Mock classes for when SQLAlchemy is not available
    class Base:
        pass
    class User:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

if SQLALCHEMY_AVAILABLE:
    Base = declarative_base()
    engine = None
    SessionLocal = None

    class User(Base):
        """User model for testing database operations."""
        __tablename__ = 'users'
        
        id = Column(Integer, primary_key=True)
        email = Column(String(255), unique=True, nullable=False)
        name = Column(String(255), nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow)
        metadata = Column(Text)
else:
    # Mock database setup when SQLAlchemy is not available
    Base = None
    engine = None
    SessionLocal = None

def init_db():
    """Initialize database connection and create tables."""
    global engine, SessionLocal
    
    if not SQLALCHEMY_AVAILABLE:
        print("Warning: SQLAlchemy not available. Database operations will be mocked.")
        return
    
    try:
        engine = create_engine(Config.DATABASE_URL, echo=False)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Add some test data
        _create_test_data()
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise

def _create_test_data():
    """Create some test data for the database."""
    db = SessionLocal()
    try:
        # Check if users already exist
        if db.query(User).count() == 0:
            test_users = [
                User(email="john@example.com", name="John Doe"),
                User(email="jane@example.com", name="Jane Smith"),
                User(email="bob@example.com", name="Bob Johnson"),
            ]
            
            for user in test_users:
                db.add(user)
            db.commit()
    except Exception as e:
        db.rollback()
        sentry_sdk.capture_exception(e)
    finally:
        db.close()

def get_user(user_id):
    """Get user by ID with potential errors."""
    if not SQLALCHEMY_AVAILABLE:
        # Mock user data
        return {
            'id': user_id,
            'email': f'user{user_id}@example.com',
            'name': f'Mock User {user_id}',
            'created_at': datetime.utcnow().isoformat()
        }
    
    db = SessionLocal()
    try:
        # Simulate random database errors
        if random.random() < 0.1:  # 10% chance of error
            raise OperationalError("Database connection lost", None, None)
        
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} not found")
        
        return {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'created_at': user.created_at.isoformat()
        }
        
    except SQLAlchemyError as e:
        sentry_sdk.capture_exception(e)
        raise
    finally:
        db.close()

def create_user(email, name):
    """Create a new user with potential constraint errors."""
    if not SQLALCHEMY_AVAILABLE:
        # Mock user creation
        return {
            'id': random.randint(1, 1000),
            'email': email,
            'name': name,
            'created_at': datetime.utcnow().isoformat()
        }
    
    db = SessionLocal()
    try:
        # Simulate random database errors
        if random.random() < 0.05:  # 5% chance of error
            raise OperationalError("Database connection timeout", None, None)
        
        user = User(email=email, name=name)
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'created_at': user.created_at.isoformat()
        }
        
    except IntegrityError as e:
        db.rollback()
        sentry_sdk.capture_exception(e)
        raise Exception(f"User with email {email} already exists")
    except SQLAlchemyError as e:
        db.rollback()
        sentry_sdk.capture_exception(e)
        raise
    finally:
        db.close()

def get_all_users():
    """Get all users with potential query errors."""
    if not SQLALCHEMY_AVAILABLE:
        # Mock user list
        return [
            {
                'id': 1,
                'email': 'john@example.com',
                'name': 'John Doe',
                'created_at': datetime.utcnow().isoformat()
            },
            {
                'id': 2,
                'email': 'jane@example.com',
                'name': 'Jane Smith',
                'created_at': datetime.utcnow().isoformat()
            }
        ]
    
    db = SessionLocal()
    try:
        # Simulate slow query
        if random.random() < 0.1:  # 10% chance of slow query
            import time
            time.sleep(2)
        
        users = db.query(User).all()
        
        return [
            {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'created_at': user.created_at.isoformat()
            }
            for user in users
        ]
        
    except SQLAlchemyError as e:
        sentry_sdk.capture_exception(e)
        raise
    finally:
        db.close()

def update_user(user_id, **kwargs):
    """Update user with potential errors."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} not found")
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        db.commit()
        db.refresh(user)
        
        return {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'created_at': user.created_at.isoformat()
        }
        
    except SQLAlchemyError as e:
        db.rollback()
        sentry_sdk.capture_exception(e)
        raise
    finally:
        db.close()

def delete_user(user_id):
    """Delete user with potential errors."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} not found")
        
        db.delete(user)
        db.commit()
        
        return {'message': f'User {user_id} deleted successfully'}
        
    except SQLAlchemyError as e:
        db.rollback()
        sentry_sdk.capture_exception(e)
        raise
    finally:
        db.close()
