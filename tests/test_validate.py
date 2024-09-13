import unittest
import json
from app import create_app

class TestValidateEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_validate_ip(self):
        """Test the IP validation endpoint with a valid IPv4 address."""
        response = self.client.post('/v1/tools/validate', json={'ip': '192.168.0.1'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['status'])

    def test_validate_ip_invalid(self):
        """Test the IP validation endpoint with an invalid IPv4 address."""
        response = self.client.post('/v1/tools/validate', json={'ip': '999.999.999.999'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data['status'])

if __name__ == '__main__':
    unittest.main()
