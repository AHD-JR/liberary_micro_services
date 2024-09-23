from bson import ObjectId
from schema import BookResponseModel, BookStatusEnum, BorrowedBookResponseModel, CategoryEnum
from typing import List
from repository import BookStore
from serializer import Serialzer
from datetime import datetime
import requests
import http_response

class Book():
    def __init__(self) -> None:
        self.book_store_helper = BookStore() 
        self.serializer = Serialzer()

    async def add_book(self, book: dict) -> str:
        try:
            # verify category
            category = book.get('category').lower()
            category_exist = any(category == item.value for item in CategoryEnum)
            if not category_exist:
                return http_response.response(status_code=400, message="Category is not recognized")

            # store book
            book['title'] = book.get('title').title()
            book['category'] = category
            book['status'] = BookStatusEnum.available
            book['created_at'] = datetime.now()
            new_book = await self.book_store_helper.store_book(book)
            if not new_book.inserted_id:
                return http_response.response(status_code=500, message="Book not added!")
            
            return http_response.response(status_code=201, message="Book Added", data={"book_id": str(new_book.inserted_id)})
        except Exception as e:
            return http_response.response(status_code=500, message=f"Error {str(e)}")

    async def remove_book(self, book_id) -> str:
        try:
           # search for the book by id
           book = await self.book_store_helper.find_book(book_id)
           if not book:
               return http_response.response(status_code=404, message="Book not found!")
           
           # remove the book
           await self.book_store_helper.remove_book(book_id)
           
           return http_response.response(status_code=200, message=f"{book['title']} removed sucessfully!")
        except Exception as e:
            return http_response.response(status_code=500, message=f"Error {str(e)}")

    async def get_book(self, book_id) -> BookResponseModel:
        try:
           # search for the book by id
           book = await self.book_store_helper.find_book(book_id)
           if not book:
               return http_response.response(status_code=404, message="Book not found!")
           
           return http_response.response(status_code=200, message="Book found", data=self.serializer.serialize_book(book))
        except Exception as e:
            return http_response.response(status_code=500, message=f"Error {str(e)}")   

    async def get_available_books(self, page, limit) -> str | List[BookResponseModel]:
        try:
           # filter by by status
           filter = {"status": BookStatusEnum.available}

           availabe_books = await self.book_store_helper.find_books(page, limit, filter)
           if not availabe_books:
               return http_response.response(status_code=404, message="No books avalable")
           
           serialized_books = [self.serializer.serialize_book(book) for book in availabe_books] 

           return http_response.response(status_code=200, message="Books fetched", data=serialized_books)
        except Exception as e:
            return http_response.response(status_code=500, message=f"Error {str(e)}")
        
    async def get_unavailable_books(self, page, limit) -> str | List[BookResponseModel]:
        try:
           # filter by by status
           filter = {"status": BookStatusEnum.borrowed}

           unavailable_books = await self.book_store_helper.find_books(page, limit, filter)
           if not unavailable_books:
               return http_response.response(status_code=404, message="No borrowed books")
           
           serialized_books = [self.serializer.serialize_book(book) for book in unavailable_books] 
           
           return http_response.response(status_code=200, message="Books fetched", data=serialized_books)
        except Exception as e:
            return http_response.response(status_code=500, message=f"Error {str(e)}")

    async def filter_by_category(self, category, page, limit) -> str | List[BookResponseModel]:
        try:
           # filter by by status
           filter = {"category": category.lower()}

           books = await self.book_store_helper.find_books(page, limit, filter)
           if not books:
               return http_response.response(status_code=404, message="No books")
           
           serialized_books = [self.serializer.serialize_book(book) for book in books] 

           return http_response.response(status_code=200, message="Books fetched", data=serialized_books)
        except Exception as e:
            return http_response.response(status_code=500, message=f"Error {str(e)}")
        
    async def filter_by_publisher(self, publisher, page, limit) -> str | List[BookResponseModel]:
        try:
           # filter by by status
           filter = {"publisher": publisher.title()}

           books = await self.book_store_helper.find_books(page, limit, filter)
           if not books:
               return http_response.response(status_code=404, message="No books")
           
           serialized_books = [self.serializer.serialize_book(book) for book in books] 

           return http_response.response(status_code=200, message="Books fetched", data=serialized_books)
        except Exception as e:
            return http_response.response(status_code=500, message=f"Error {str(e)}")
        
    # borrowed bookes and users that borrowed them
    async def get_borrowed_books(self, page, limit) -> str | List[BorrowedBookResponseModel]:
        try:
           data = await self.book_store_helper.find_borrowed_books(page, limit)
           if not data:
               return http_response.response(status_code=404, message="No book borrowed by any user!")
           
           serialized_data = [self.serializer.serialize_borrow_data(record) for record in data]

           return http_response.response(status_code=200, message="Users fetched", data=serialized_data)
        except Exception as e:
            return http_response.response(status_code=500, message=f"Error {str(e)}")

    async def borrow_book(self, borrow_data_dict) -> str:
        try:
            if borrow_data_dict["days"] <= 0:
                return http_response.response(status_code=400, message="Rent days must be at least 1")

            book = await self.book_store_helper.find_book(borrow_data_dict["book_id"])
            if not book:
                return http_response.response(status_code=404, message="No such book")
            if book['status'] == BookStatusEnum.borrowed:
                return http_response.response(status_code=409, message="Book is not available for borrow!")
            
            borrow_data_dict['book_id'] = ObjectId(borrow_data_dict.get('book_id'))
            borrow_data_dict['borrow_date'] = datetime.now()
            
            new_borrow = await self.book_store_helper.store_borrow_data(borrow_data_dict)
            if not new_borrow.inserted_id:
               return http_response.response(status_code=500, message="Book not borrowed")
            
            # change book status
            data = {"status": BookStatusEnum.borrowed}
            await self.book_store_helper.update_book(borrow_data_dict['book_id'], data)

            return http_response.response(status_code=200, message="Users fetched", data={"borrow_record_id": str(new_borrow.inserted_id)})
        except Exception as e:
            return http_response.response(status_code=500, message=f"Error {str(e)}")

    async def get_all_users(self, page, limit):
        try:
            url = f"http://frontend:8001/users/"

           # Define the query parameters
            params = {
                'offset': page - 1,
                'limit': limit
            }

            response = requests.get(url, params=params)
            if response.status_code == 404:
                error_massage = response.json()['message']
                return http_response.response(status_code=404, message=error_massage)
            response.raise_for_status()  # Raises an error for HTTP errors

            # Parse the JSON response
            data = response.json()
            
            return data
        except Exception as e:
            return http_response.response(status_code=500, message=f"Error {str(e)}")

""" 
def _generate_book_id(self, title, category, publisher):
        '''for uniqueness, book_id is generated to be the first word in title, category, 
        and publisher, folloiwed by 4 random digits'''

        title_word = title.split(' ')[0]
        category_word = category.split(' ')[0]
        publisher_word = publisher.split(' ')[0]

        random_number = random.randint(1_000, 9_999)

        book_id = f"{title_word}-{category_word}-{publisher_word}-{random_number}"

        return book_id
"""
