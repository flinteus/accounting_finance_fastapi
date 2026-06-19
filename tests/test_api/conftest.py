import sys
import os

# настройка скоупа
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, root)


from typing import Generator
from fastapi.testclient import TestClient
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from main import app
from app.dependecy import get_db
from app.database import Base
from app.models import User, Wallet



TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine("sqlite:///./test.db",
                            connect_args={"check_same_thread": False})

TestSessionLocal = sessionmaker(autocommit=False, 
                                autoflush=False, 
                                bind=test_engine)


def get_test_db() -> Generator[Session, None, None]:
    db = TestSessionLocal()
    
    try:
        yield db
        
    finally:
        db.close()
        
app.dependency_overrides[get_db] = get_test_db


@pytest.fixture()
def client():
    yield TestClient(app)
    
    
@pytest.fixture(autouse=TestClient)
def setup_db():
    
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
    
    
@pytest.fixture()   
def db_session():
    
    db = TestSessionLocal()
    
    try:
        yield db
        
    finally:
        db.close()

@pytest.fixture
def user_with_wallet(db_session):

    user = User(login="test")
    db_session.add(user)
    db_session.flush()
    
    wallet = Wallet(name="card", balanse=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)
    
    return user, wallet
    
