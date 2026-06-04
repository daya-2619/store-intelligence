import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
import os

# Create an in-memory SQLite database
engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# We must mock SessionLocal wherever it is imported.
@pytest.fixture(autouse=True)
def mock_db_session(monkeypatch):
    monkeypatch.setattr("app.db.SessionLocal", TestingSessionLocal)
    monkeypatch.setattr("app.services.funnel_service.SessionLocal", TestingSessionLocal)
    monkeypatch.setattr("app.services.session_service.SessionLocal", TestingSessionLocal)
    monkeypatch.setattr("app.services.metrics_service.SessionLocal", TestingSessionLocal)
    monkeypatch.setattr("app.services.transaction_service.SessionLocal", TestingSessionLocal)
    monkeypatch.setattr("app.services.ingestion_service.SessionLocal", TestingSessionLocal)
    
@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
