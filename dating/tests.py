import time
import jwt
from django.test import TestCase
from .helpers import jwt_encode, jwt_decode


class JWTTestCase(TestCase):
    def setUp(self):
        pass

    def test_jwt(self):
        token = jwt_encode({
            "payload": 1234,
            "exp": int(time.time() + 60*60*24*60)
            })
        self.assertTrue(isinstance(token, str))
        info = jwt_decode(token)
        self.assertTrue(isinstance(info, dict))
        self.assertEqual(info['payload'], 1234)

    def test_expire(self):
        token = jwt_encode({
            "payload": 1234,
            "exp": int(time.time() - 1)
            })

        with self.assertRaises(jwt.exceptions.ExpiredSignatureError):
            _ = jwt_decode(token)
