import logging

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import Dict
import uvicorn

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI()


books = {
    1: {
        'title': 'Richard Montes',
        'author': 'William Clark',
        'publisher': 'Mcneil, Hall and Duke',
        'publisher_date': '2022-11-12',
        'page_count': 135,
        'language': 'Albanian'
    },
    2: {
        'title': 'Steven Owen',
        'author': 'Christopher Smith',
        'publisher': 'Anderson, Stewart and Cooper',
        'publisher_date': '1991-08-18',
        'page_count': 248,
        'language': 'Tibetan'
    },
    3: {
        'title': 'Lorraine Gonzalez',
        'author': 'Michael Thornton',
        'publisher': 'Allen, Kennedy and Brady',
        'publisher_date': '2020-07-31',
        'page_count': 139,
        'language': 'Malagasy'
    },
    4: {
        'title': 'Candace Burns',
        'author': 'Roger Hill',
        'publisher': 'Hudson LLC',
        'publisher_date': '1992-07-08',
        'page_count': 102,
        'language': 'Tigrinya'
    },
    5: {
        'title': 'Paul Howard MD',
        'author': 'Lucas Brooks',
        'publisher': 'Cohen, Logan and Carter',
        'publisher_date': '1970-07-20',
        'page_count': 187,
        'language': 'Kashmiri'
    },
    6: {
        'title': 'Matthew Carey',
        'author': 'Michael Joseph',
        'publisher': 'Reid, Gilbert and Padilla',
        'publisher_date': '2014-07-12',
        'page_count': 139,
        'language': 'Bihari languages'
    }
}


class Book(BaseModel):
    title: str
    author: str
    publisher: str
    publisher_date: str
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    page_count: int | None = None
    language: str | None = None


@app.get('/books', response_model=Dict[int, Book])
async def get_all_book():
    return books


@app.post('/books', status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: Book) -> dict:
    new_book = book_data.model_dump()
    index = len(books) + 1
    books.update({index: new_book})

    return new_book


@app.get('/books/{book_id}')
async def get_book(book_id: int) -> dict:

    if book_id in books:
        return JSONResponse(
            content=books[book_id], 
            status_code=status.HTTP_302_FOUND
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"msg": f"Book with id {book_id} not found"}
    )


@app.patch('/pbooks/{book_id}', response_model=BookUpdateModel)
async def update_pbook(book_id: int, book: BookUpdateModel) -> JSONResponse:
    try:
        stored_book_data = books[book_id]
        stored_book_model = BookUpdateModel(**stored_book_data)
        update_data = book.model_dump(exclude_unset=True)
        updated_book = stored_book_model.model_copy(update=update_data).model_dump()
        books.update({book_id: jsonable_encoder(updated_book)})
        return JSONResponse(
            content=updated_book,
            status_code=status.HTTP_200_OK
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail={"msg": f"It was not possible to update book {book_id}"}
        )


@app.patch('/books/{book_id}')
async def update_book(book_id: int, book_update_data: BookUpdateModel) -> dict:
    if book_id in books:
        book = books[book_id]
        book['title'] = book_update_data.title
        book['author'] = book_update_data.author
        book['publisher'] = book_update_data.publisher
        book['page_count'] = book_update_data.page_count
        book['language'] = book_update_data.language

        return JSONResponse(
            content=book,
            status_code=status.HTTP_200_OK
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"msg": "Not found"}
    )


@app.delete('/books/{book_id}')
async def delete_book(book_id: int):
    if book_id in books:
        del books[book_id]
        return JSONResponse(
            content={},
            status_code=status.HTTP_200_OK
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"msg": f"Book with {book_id} not found"}
    )


if __name__ == '__main__':
    uvicorn.run(
        app='main:app', 
        log_level='debug',
        reload=True
    )
