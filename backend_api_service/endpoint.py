from fastapi import APIRouter
from schema import BookRequestModel, BorrowBookRequestModel
from controller import Book

router = APIRouter(
    tags=["Backend/Admin API Service"],
    prefix='/admin'
)

book_controller_helper = Book()

# NB: The valid categories are: 'novel', 'self help', 'fiction', 'romance', and 'others'. 
@router.post("/add_book")
async def add_book(book: BookRequestModel):
    book_dict = book.dict()
    return await book_controller_helper.add_book(book_dict)

@router.delete("/remove_book")
async def remove_book(book_id: str):
    return await book_controller_helper.remove_book(book_id)

@router.get("/users")
async def get_all_users(page: int = 1, limit: int = 20):
    return await book_controller_helper.get_all_users(page, limit)

# users and the books they have borrowed
@router.get("/books/borrowers")
async def get_borrowed_books(page: int = 1, limit: int = 20):
    return await book_controller_helper.get_borrowed_books(page, limit)

@router.get("/get_unavailable_books")
async def get_unavailable_books(page: int = 1, limit: int = 20):
    return await book_controller_helper.get_unavailable_books(page, limit)

# region for_frontend_api_service
# these endpoints are exposed for the frontent_api_service to communicate with this backend_api_service 
@router.get("/book/{book_id}")
async def get_unavailable_books(book_id):
    return await book_controller_helper.get_book(book_id)

@router.get("/get_available_books")
async def get_unavailable_books(page: int = 1, limit: int = 20):
    return await book_controller_helper.get_available_books(page, limit)

@router.get("/books/category/{category}")
async def filter_by_category(category, page: int = 1, limit: int = 20):
    return await book_controller_helper.filter_by_category(category, page, limit)

@router.get("/books/publisher/{publisher}")
async def filter_by_publisher(publisher, page: int = 1, limit: int = 20):
    return await book_controller_helper.filter_by_publisher(publisher, page, limit)

@router.post("/books/borrow_book")
async def borrow_book(request_body: BorrowBookRequestModel):
    return await book_controller_helper.borrow_book(request_body.dict())

# endregion
