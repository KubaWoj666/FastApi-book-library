# Book Library REST API
REST API for online library. It supports authors of books and books resources including Oauth2 authentication (JWT Token).

The documentation can be found in documentation.html or here

## Setup
- Clone repository
- Create database and user
- Rename .env.example to .env and set your values

# SQLALCHEMY_DATABASE_URL MySQL template
SQLALCHEMY_DATABASE_URL=f"mysql+mysqlconnector://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
- Create a virtual environment <br />
python -m venv venv
- Activate virtual environment (in VsCode)<br />
source venv/bin/activate
- Install packages from requirements.txt<br />
pip install -r requirements.txt
- Migrate database<br />
alembic upgrade head
- Run server by command<br />
uvicorn app.main:app --reload  
- Load sample data <br />


# Tests (in future)
In order to execute tests located in tests<br /> 
run the command:<br />
python -m pytest tests/

# Technologies / Tools
- Python 3.10
- FastApi
- alembic 1.9.2
- SQLAlchemy 1.4.46
- pytest==7.2.1
- MySQL
- Heroku
- Postman