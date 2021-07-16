import unittest
from backend import app


class BaseTestClass(unittest.TestCase):
    def setUp(self):
        """
        set up de la app.
        :returns: None
        """
        self.app = app
        self.client = self.app.test_client()
        # Crea un contexto de aplicación
        with self.app.app_context():
            pass
            # Crea las tablas de la base de datos
            # db.create_all()
    
    def test_index_with_no_posts(self):
        """
        check if the app are connected.
        :returns: two asserts assert in and assert equal
        """
        res = self.client.get('/')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'pong', res.data)

    def test_get_all_process(self):
        """
        check all the process.
        :returns: two asserts assertIsInstance and assertEqual
        """
        res = self.client.get('/processes')
        self.assertEqual(200, res.status_code)
        self.assertIsInstance(res.data, (bytes,))

    # def test_create_process(self):
    #     """
    #     create a process.
    #     :returns: two asserts assert in and assert equal
    #     """
    #     res = self.client.post('/process', data = dict(
    #         name = "prueba",
    #         status = "prueba",
    #         time_execution = "prueba"
    #     ))
    #     self.assertEqual(200, res.status_code)



if __name__ == "__main__":
    unittest.main()