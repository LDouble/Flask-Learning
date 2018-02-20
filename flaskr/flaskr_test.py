import os
import flaskr
import unittest
import tempfile


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.testing = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data

    def login(self):
        return self.app.post("/login", data={
            "username": "admin",
            "password": "password",
        }, follow_redirects=True)

    def logout(self):
        return self.app.get("/logout", follow_redirects=True)

    def test_login_logout(self):
        rv = self.login()
        assert "注销".encode(encoding="UTF-8") in rv.data
        rv = self.logout()
        print(rv.data)
        assert "登陆".encode(encoding="UTF-8") in rv.data


if __name__ == "__main__":
    unittest.main()