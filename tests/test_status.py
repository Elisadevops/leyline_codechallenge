import unittest
import json
from app import create_app

class TestStatusEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_root_status(self):
        """Test the root endpoint for status, version, date, and Kubernetes status."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('version', data)
        self.assertIn('date', data)
        self.assertIn('kubernetes', data)

if __name__ == '__main__':
    unittest.main()
