import unittest
from src.main import get_repositories
from unittest.mock import patch

class TestMain(unittest.TestCase):

    # Test if an error is raised when an invalid user is provided
    @patch('builtins.print')  # Mock the print function to suppress output during the test
    def test_get_repositories_invalid_user(self, mock_print):
        with self.assertRaises(SystemExit):  # The function should call sys.exit(1) when the API request fails
            get_repositories("invalid_user_123")

if __name__ == "__main__":
    unittest.main()
