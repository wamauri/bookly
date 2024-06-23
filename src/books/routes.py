import logging

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import APIRouter, status
from typing import Dict

from src.books.schemas import Book, BookUpdateModel
from src.books.book_data import books

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

book_router = APIRouter()


@book_router.get('/', response_model=Dict[int, Book])
async def get_all_book():
    logger.debug("Get all books in schemas...")
    return books


@book_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: Book) -> dict:
    logger.debug("Creating a new book...")
    new_book = book_data.model_dump()
    index = len(books) + 1
    books.update({index: new_book})

    return new_book


@book_router.get('/{book_id}')
async def get_book(book_id: int) -> dict:
    logger.debug("Getting a book...")
    if book_id in books:
        return JSONResponse(
            content=books[book_id], 
            status_code=status.HTTP_302_FOUND
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"msg": f"Book with id {book_id} not found"}
    )


@book_router.patch('/partial/{book_id}', response_model=BookUpdateModel)
async def update_pbook(book_id: int, book: BookUpdateModel) -> JSONResponse:
    logger.debug("Partial updating a book...")
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


@book_router.patch('/{book_id}')
async def update_book(book_id: int, book_update_data: BookUpdateModel) -> dict:
    logger.debug("Updating a book...")
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


@book_router.delete('/{book_id}')
async def delete_book(book_id: int):
    logger.debug("Deleting a book...")
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
