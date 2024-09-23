from schema import UserRequestModel, BookResponseModel, BorrowRequestModel
from typing import List
from repository import UsersStore
from datetime import datetime
from serializer import Serialzer
import requests
import http_response # my costume response module

class User():
    def __init__(self) -> None:
        self.user_store_helper = UsersStore()
        self.serializer = Serialzer()

    def create_user(self, user_data) -> str:
        try:
           user = self.user_store_helper.find_user_by_email(user_data['email'])
           if user:
               return http_response.response(status_code=409, message="Email has been taken!")

           user_data["created_at"] = datetime.now()

           new_user = self.user_store_helper.store_user(user_data)

           # serialize datetime
           new_user['created_at'] = str(new_user.get('created_at'))
        
           return http_response.response(status_code=201, message="Account has been created", data=new_user)
        except Exception as e:
            return http_response.response(status_code=500, message=f"Error {str(e)}")

    def get_all_users(self, limit, offset) -> str | List[UserRequestModel]:
        try:
           users = self.user_store_helper.find_users(limit, offset)
           if not users:
               return http_response.response(status_code=404, message="No users!")
           
           serialized_users = [self.serializer.serialize_user(user) for user in users]

           return http_response.response(status_code=200, message="Users fetched", data=serialized_users)
        except Exception as e:
            return http_response.response(status_code=500, message=f"Error {str(e)}")
        
    def get_user(self, email) -> str | UserRequestModel:
        try:
           user = self.user_store_helper.find_user_by_email(email)
           if not user:
               return http_response.response(status_code=404, message="No such user!")
           
           return http_response.response(status_code=200, message="Users fetched", data=self.serializer.serialize_user(user))
        except Exception as e:
            return http_response.response(status_code=500, message=f"Error {str(e)}")
        
    def get_books(self, limit, offset) -> str | List[BookResponseModel]:
        try:
            url = f"http://backend:8000/admin/get_available_books"

           # Define the query parameters
            params = {
                'page': offset + 1,
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

    def get_books_by_category(self, category, limit, offset) -> str | List[BookResponseModel]:
        try:
            url = f"http://backend:8000/admin/books/category/{category}"

           # Define the query parameters
            params = {
                'page': offset + 1,
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
        
    def get_books_by_publisher(self, publisher, limit, offset) -> str | List[BookResponseModel]:
        try:
            url = f"http://backend:8000/admin/books/publisher/{publisher}"

           # Define the query parameters
            params = {
                'page': offset + 1,
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
        
    def get_book_by_id(self, book_id) -> str | List[BookResponseModel]:
        try:
            url = f"http://backend:8000/admin/book/{book_id}"

            response = requests.get(url)
            if response.status_code == 404:
                error_massage = response.json()['message']
                return http_response.response(status_code=404, message=error_massage)
            response.raise_for_status()  # Raises an error for HTTP errors

            # Parse the JSON response
            data = response.json()
            
            return data
        except Exception as e:
            return http_response.response(status_code=500, message=f"Error {str(e)}")

    def borrow_book(self, payload: BorrowRequestModel) -> str | List[BookResponseModel]:
            try:
                # verify if user exists
                user = self.user_store_helper.find_user_by_email(payload['email'])
                if not user:
                    return "User does not exist"
                 
                url = "http://backend:8000/admin/books/borrow_book"

                response = requests.post(url, json=payload)
                if response.status_code == 400 or response.status_code == 404 or response.status_code == 409:
                    status_code = response.status_code
                    error_massage = response.json()['message']
                    return http_response.response(status_code=status_code, message=error_massage)
                response.raise_for_status()  # Raises an error for HTTP errors

                # Parse the JSON response
                data = response.json()
                
                return data
            except Exception as e:
                return http_response.response(status_code=500, message=f"Error {str(e)}")

