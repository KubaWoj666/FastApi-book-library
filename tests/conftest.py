from fastapi.testclient import TestClient
import pytest
from app.main import app
from app .config import settings
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.oauth2 import create_access_token
from app import models




SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]= override_db
    yield TestClient(app)
