import jwt
import time


headers = {
    "alg": "HS256",
    "typ": "JWT"
}

salt = "icfwwhxuylfjrbbhxtdsxhyrihgtcogfwyjdcamawvgcdkmzkrdcqawtqrzfqoypwri"


def jwt_encode(payload):
    '''
    Encode JWT token

    **Parameters**

        payload: *dict*
            The info to encode (contains "exp" value to set expiration)

    **Returns**

        token: *str*
            Generated JWT token

    '''
    return jwt.encode(
        payload=payload,
        key=salt,
        algorithm='HS256',
        headers=headers).decode('utf-8')


def jwt_decode(token):
    '''
    Decode JWT token

    **Parameters**

        token: *str*
            JWT token

    **Returns**

        token: *dict*
            Decoded info

    '''
    return jwt.decode(token, salt, True, algorithm='HS256')
