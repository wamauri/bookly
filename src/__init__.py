from fastapi import FastAPI
import uvicorn

from src.books.routes import book_router
from utils.headers import headers

version = 'v1'
app = FastAPI(
    title='Bookly',
    description='A REST API for a book review web service',
    version=version
)
app.include_router(
    router=book_router, 
    prefix=f'/api/{version}/books',
    tags=['books']
)
app.include_router(
    router=headers, 
    prefix=f'/api/{version}/headers',
    tags=['headers']
)

if __name__ == '__main__':
    uvicorn.run(
        app='main:app', 
        log_level='debug',
        reload=True
    )
