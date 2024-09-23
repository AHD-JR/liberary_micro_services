from fastapi import APIRouter
from schema import UserRequestModel, BorrowRequestModel
from controller import User

router = APIRouter(
    tags=["Frontend API Service"],
    prefix='/users'
)

user_controller_helper = User()

@router.post("/create_user")
def create_user(user: UserRequestModel):
    user_dict = user.dict()
    return user_controller_helper.create_user(user_dict)

# get avalable books
@router.get("/available_books")
def get_books(limit: int = 10, offset: int = 0):
    return user_controller_helper.get_books(limit, offset)

@router.get("/book/{book_id}")
def get_book(book_id):
    return user_controller_helper.get_book_by_id(book_id)

# books fltered by publisher
@router.get("/books/publisher/{publisher}")
def get_books_by_publisher(publisher, limit: int = 10, offset: int = 0):
    return user_controller_helper.get_books_by_publisher(publisher, limit, offset)

# books fltered by category
@router.get("/books/catgory/{catgory}")
def get_books_by_category(category, limit: int = 10, offset: int = 0):
    return user_controller_helper.get_books_by_category(category, limit, offset)

@router.post("/borrow_book")
def borrow_book(request_body: BorrowRequestModel):
    return user_controller_helper.borrow_book(request_body.dict())

# region for_backend_api_service
# this endpoint is exposed for the backend_api_service to communicate with this frontent_api_service
@router.get("/")
def get_users(limit: int = 10, offset: int = 0):
    return user_controller_helper.get_all_users(limit, offset)

"""@router.get("/{email}")
def get_user(email):
    return user_controller_helper.get_user(email)
"""

# endregion
