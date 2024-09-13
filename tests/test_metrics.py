import unittest
from app import create_app

class TestMetricsEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_metrics_endpoint(self):
        """Test the /metrics endpoint for Prometheus metrics."""
        response = self.client.get('/metrics')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
