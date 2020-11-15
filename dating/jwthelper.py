import jwt
import time

headers = {
  "alg": "HS256",
  "typ": "JWT"
}

salt = "icfwwhxuylfjrbbhxtdsxhyrihgtcogfwyjdcamawvgcdkmzkrdcqawtqrzfqoypwrirkgsekrtgxsdqjnycxskpygeeqjzorexa"

def jwt_encode(payload):
  return jwt.encode(payload=payload, key=salt, algorithm='HS256', headers=headers).decode('utf-8')

def jwt_decode(token):
  return jwt.decode(token, salt, True, algorithm='HS256')
