import unittest
import json
from app import create_app, db

class TestHistoryEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_query_history(self):
        """Test the query history endpoint."""
        # Perform a lookup query to generate some history
        self.client.get('/v1/tools/lookup?domain=example.com')

        # Retrieve the latest 20 queries
        response = self.client.get('/v1/history')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertLessEqual(len(data), 20)

if __name__ == '__main__':
    unittest.main()
