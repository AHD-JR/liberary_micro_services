from mongo_db_config import books_collection, borrow_data_collection
from bson import ObjectId

class BookStore():
    def __init__(self) -> None:
        pass

    async def store_book(self, book):
        return await books_collection.insert_one(book)

    async def remove_book(self, book_id):
        return await books_collection.delete_one({'_id': ObjectId(book_id)})

    async def find_book(self, book_id):
        return await books_collection.find_one({'_id': ObjectId(book_id)})

    async def find_books(self, page, limit, filter=None):
        # query based on filter if filter is set
        if not filter:
            filter = {}

        return await books_collection.find(filter).skip((page - 1) * limit).limit(limit).to_list(limit)

    async def store_borrow_data(self, borrow_dict):
        return await borrow_data_collection.insert_one(borrow_dict)
    
    async def find_borrowed_books(self, page, limit):
        pipeline = [
            {
                "$match": {}
            },
            {
                "$sort": {
                    "created_at": -1
                }
            },
            {
                "$skip": (page - 1) * limit
            },
            {
                "$limit": limit
            },
            {
                "$lookup": {
                    "from": "books",
                    "localField": "book_id",
                    "foreignField": "_id",
                    "as": "books"
                }
            },
            {
                "$unwind": "$books"
            },
            {
                "$project": {
                    "_id": 1,  
                    "book_id": 1,
                    "book_title": "$books.title",
                    "book_category": "$books.category",
                    "book_publisher": "$books.publisher",
                    "email": 1,
                    "borrow_date": 1,
                    "days": 1
                }
            }
        ]
        
        return await borrow_data_collection.aggregate(pipeline).to_list(limit)

    async def update_book(self, book_id, data):
        return books_collection.update_one({'_id': ObjectId(book_id)}, {'$set': data})

    async def get_books_count(filter: dict=None):
        if not filter:
            filter = {}
        return await books_collection.count_documents(filter)