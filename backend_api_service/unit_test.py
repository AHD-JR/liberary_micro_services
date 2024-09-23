import unittest
from unittest.mock import patch, MagicMock
from repository import BookStore
from datetime import datetime

class TestBookStore(unittest.TestCase):
    @patch('repository.MongoClient')  # Mock MongoClient to avoid real MongoDB calls
    def test_store_book(self, mock_mongo_client):
        # Arrange
        mock_db = MagicMock()  # Mock the MongoDB database
        mock_collection = MagicMock()  # Mock the books collection
        mock_mongo_client.return_value.__getitem__.return_value = mock_db  # Mock database access
        mock_db.__getitem__.return_value = mock_collection  # Mock collection access
        
        bookstore = BookStore()  # BookStore instance
        book_data = {
            'title': 'Test Book Title',
            'category': 'Science Fiction',
            'publisher': 'Test Publisher'
        }

        # Act
        bookstore.store_book(book_data)

        # Assert
        mock_collection.insert_one.assert_called_once()  # Ensure insert_one was called
        args, kwargs = mock_collection.insert_one.call_args  # Retrieve the call arguments
        inserted_book = args[0]  # Get the first argument (the inserted book)
        
        # Check that the 'created_at' field was added to the book object
        self.assertIn('created_at', inserted_book)
        self.assertIsInstance(inserted_book['created_at'], datetime)
        self.assertEqual(inserted_book['title'], 'Test Book Title')
        self.assertEqual(inserted_book['category'], 'Science Fiction')
        self.assertEqual(inserted_book['publisher'], 'Test Publisher')

if __name__ == '__main__':
    unittest.main()
