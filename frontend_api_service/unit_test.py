import unittest
from unittest.mock import MagicMock, patch
from sqlite_config import User
from repository import UsersStore  # Ensure this path is correct
from datetime import datetime

class TestUsersStore(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.user_store_helper = UsersStore()

    @patch('repository.SessionLocal')  # Mock SessionLocal to avoid actual DB interaction
    @patch.object(UsersStore, 'close')  # Mock close to prevent closing the mock session
    def test_store_user(self, mock_close, mock_session):
        # Arrange
        mock_db = MagicMock()  # Mock the session object
        mock_session.return_value = mock_db  # Use the mock session for UsersStore
        
        user_data = {  # Sample user data
            'email': 'test@example.com', 
            'first_name': 'Firstname', 
            'last_name': 'Lastname',
            'created_at': datetime.now()
        }

        # Act
        self.user_store_helper.store_user(user_data)

        # Assert
        mock_db.add.assert_called_once()  # Check if the add method was called once
        mock_db.commit.assert_called_once()  # Check if the commit method was called once
        mock_db.refresh.assert_called_once()  # Check if refresh was called once

        added_user = mock_db.add.call_args[0][0]  # Get the user object passed to add
        self.assertEqual(added_user.email, 'test1@example.com')
        self.assertEqual(added_user.first_name, 'Firstname')
        self.assertEqual(added_user.last_name, 'Lastname')

        # Ensure close was called once
        mock_close.assert_called_once()

# Run the test
if __name__ == '__main__':
    unittest.main()
