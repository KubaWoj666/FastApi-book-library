from fastapi import APIRouter, Depends, status
from ..database import get_db
from sqlalchemy.orm import Session
from datetime import datetime
from app.models import Author, Book
import json
from pathlib import Path

router = APIRouter(
    prefix="/sample/data",
    tags=["Sample data"]
)


def load_json_data(file_name: str) -> list:
    json_path = Path(__file__).parent.parent.parent / "samples" / file_name
    with open(json_path) as file:
        data_json = json.load(file)
        print(data_json)
    return data_json



@router.post("/add", status_code=status.HTTP_200_OK)
def add_authors_sample_data(db:Session = Depends(get_db)):
    try:
        data_json = load_json_data("authors.json")
        for item in data_json:
            item['birth_date'] = datetime.strptime(item['birth_date'], '%d-%m-%Y').date()
            author = Author(**item)
            db.add(author)
        data_json = load_json_data("books.json")
        for item in data_json:
            book = Book(**item)
            db.add(book)
        db.commit()
        db.refresh(author)
        db.refresh(book)
        return {"massage" : "Data hes been successfully added to database" }
    except Exception as exe:
        return { "massage": "Unexpected error: {}".format(exe)}




@router.delete("/delete", status_code=status.HTTP_200_OK)
def delete_data(db:Session=Depends(get_db)):
    """Delate data form database"""
    try:
        db.execute('DELETE FROM books')
        db.execute('ALTER TABLE books AUTO_INCREMENT = 1')
        db.execute('DELETE FROM authors')
        db.execute('ALTER TABLE authors AUTO_INCREMENT =1')
        db.commit()
        return{"massage" : "Data hes been successfully deleted"}
    except Exception as exe:
        return {"massage": "Unexpected error: {}".format(exe)}
    