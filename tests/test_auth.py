import unittest

from app import db
from app.models import User


class UserModelCase(unittest.TestCase):
    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))
