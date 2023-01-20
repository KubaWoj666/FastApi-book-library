import json
from datetime import datetime
from pathlib import Path

import click
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.main import app
from app.models import Authors

# db : Session = Depends(get_db)

@app.dependency_overrides()
def get_db_function(db: Session = Depends(get_db)):
    return db

def load_json_data(file_name: str) -> list:
    json_path = Path(__file__).parent / "samples" / file_name
    with open(json_path) as file:
        data_json = json.load(file)
    return data_json

@click.group()
def db_manage():
    """database management comments"""
    pass

@db_manage.command()
def add_data():
    db = get_db_function()
    
    try:
        data_json = load_json_data("authors.json")
        for item in data_json:
            item['birth_date'] = datetime.strptime(item['birth_date'], '%d-%m-%Y').date()
            author = Authors(**item)
            db.add(author)
        db.commit()
        db.refresh(author)
        click.echo("Data hes been successfully added to database")
    except Exception as exe:
        click.echo("Unexpected error: {}".format(exe))

    
    

@db_manage.command()
def delete_data():
    """Delate data form database"""
    click.echo('Dropped the database')

if __name__ == '__main__':
    db_manage()