from fastapi import APIRouter, Depends, HTTPException, status, Response
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder



router = APIRouter(
    prefix="/author",
    tags=["Authors"]
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.AuthorsSchema])
def get_all_authors(db:Session = Depends(get_db)):
    authors = db.query(models.Author).all()
    # return JSONResponse({
    #     "success": True,
    #     "data": jsonable_encoder(authors),
    #     "number_of_records": len(authors)
    # })
    return authors



@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.AuthorsSchema)
def get_singe_author(id:int, db: Session=Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == id).first()


    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Author with id: {id} dose not exists!")

    return JSONResponse({
        "success": True,
        "data": jsonable_encoder(author)
        })
    

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.AuthorsSchema)
def create_author(author: schemas.CreateAuthorSchema, db:Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):

    author = models.Author(**author.dict())
    db.add(author)
    db.commit()
    db.refresh(author)
    

    return JSONResponse({
        "success": True,
        "data": jsonable_encoder(author)})


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.CreateAuthorSchema)
def update_author(id: int, update_author:schemas.CreateAuthorSchema, db:Session= Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
    author_query = db.query(models.Author).filter(models.Author.id == id)
    author = author_query.first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Author with id: {id} dose not exists!")


    author_query.update(update_author.dict(), synchronize_session=False)
    db.commit()

    return update_author



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_author(id: int, db:Session=Depends(get_db),  current_user:int=Depends(oauth2.get_current_user)):
    author_query = db.query(models.Author).filter(models.Author.id == id)
    author = author_query.first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"success" : False, "message":  f"Author with id: {id} dose not exists!"})

    author_query.delete(synchronize_session=False)
    db.commit()

    return JSONResponse({
        "success" : True,
        "message": f"Author with id {id} successful deleted"
    })