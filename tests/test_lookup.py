import unittest
import json
from app import create_app

class TestLookupEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_lookup_domain(self):
        """Test the domain lookup endpoint with a valid domain."""
        response = self.client.get('/v1/tools/lookup?domain=example.com')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('addresses', data)
        self.assertIsInstance(data['addresses'], list)

    def test_lookup_domain_invalid(self):
        """Test the domain lookup endpoint with an invalid domain."""
        response = self.client.get('/v1/tools/lookup?domain=invalid-domain')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
