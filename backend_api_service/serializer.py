from datetime import timedelta

class Serialzer():
    def __init__(self) -> None:
        pass

    def serialize_book(self, book):
        return {
        'id': str(book.pop('_id')),
        'created_at': str(book.pop('created_at')),
        **book
    }   

    def serialize_borrow_data(self, borrow_data):
        # compute the return date based on days specified by the user during borrowing 
        return_date = borrow_data.get('borrow_date') + timedelta(borrow_data.get('days'))
        return {
            "id": str(borrow_data.pop('_id')), 
            "book_id": str(borrow_data.pop('book_id')),
            "borrow_date": str(borrow_data.pop('borrow_date')),
            "return_date": str(return_date),
            **borrow_data
        }