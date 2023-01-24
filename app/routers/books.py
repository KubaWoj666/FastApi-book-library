from fastapi import APIRouter, Depends, HTTPException, status
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError



router = APIRouter(
    prefix="/books",
    tags=["Books"]
)



@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.Books])
def get_all_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()

    return books
    # return JSONResponse({
    #     "success" : True,
    #     "data": jsonable_encoder(books),
    #     "number of records": len(books)
    # })



@router.get('/{book_id}', status_code=status.HTTP_200_OK, response_model=schemas.Books)
def get_one_book(book_id:int, db:Session=Depends(get_db)):
    book_query = db.query(models.Book).filter(models.Book.id == book_id)
    book = book_query.first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id: {book_id} dose not exist")
    
    # data = jsonable_encoder(book)
    # return JSONResponse({
    #     "successs": True,
    #     "data": data
    # })
    return book




@router.get('/author/{author_id}', status_code=status.HTTP_200_OK, response_model=List[schemas.CreateBook])
def get_all_author_book(author_id:int, db:Session=Depends(get_db)):

    author_query = db.query(models.Author).filter(models.Author.id == author_id)
    author = author_query.first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Author with id {author_id} dose not exist")

    books= db.query(models.Book).filter(models.Book.author_id == author_id).all()
    
    
    return JSONResponse({
        "success": True,
        "data": jsonable_encoder(books),
        "nuber of records": len(books)
    })



@router.post('/{author_id}', status_code=status.HTTP_201_CREATED, response_model=schemas.CreateBook)
def create_book(author_id: int, book:schemas.BookCreate, db:Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):

    author_query = db.query(models.Author).filter(models.Author.id == author_id)
    author = author_query.first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Author with id {author_id} dose not exist")

    book_query = db.query(models.Book).filter(models.Book.isbn == book.isbn)
    book_isbn = book_query.first()
    if not book_isbn:
        new_book = models.Book(author_id=author_id, **book.dict())
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Book with ISBN {book.isbn} already exist")


    # return new_book
    return JSONResponse({
        "success": True,
        "data": jsonable_encoder(new_book)
    })


@router.put("/{book_id}", status_code=status.HTTP_200_OK, response_model=schemas.CreateBook)
def update_book(book_id: int, update_book:schemas.CreateBook, db:Session=Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
    book_query = db.query(models.Book).filter(models.Book.id == book_id)
    book = book_query.first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with id: {book_id} dose not exists!")
    
    try:
        book_query.update(update_book.dict(), synchronize_session=False)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Book with isbn {update_book.isbn} already exist or author with id {update_book.author_id} dose not exist")  
    return update_book

# TODO author id validation 
    # book_query.update(update_book.dict(), synchronize_session=False)
    # author_query = db.query(models.Author).filter(models.Author.id == update_book.author_id)
    # print(author_query)
    # author = author_query.first()
    # print(update_book.author_id)
    # print(author.id)
    # if not author:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"dupa!")

    
    # return update_book



@router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id:int, db:Session=Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
    book_query = db.query(models.Book).filter(models.Book.id==book_id)
    book = book_query.first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id: {book_id} dose not exist")
    
    book_query.delete(synchronize_session=False)
    db.commit()
    return JSONResponse({
        "success": True,
        "message": f"Successful delete book with id {book_id}"
    })


