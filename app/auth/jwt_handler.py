import time
import jwt
from decouple import config
from typing import Optional
from datetime import timedelta#, datetime

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 30

def token_response(token: str):
    return {
        "access token": token
    }

def generate_access_token(data: dict):
    to_encode = data.copy()
    # if expires_delta:
    #     expire = time.time() + expires_delta
    # else:
    expire = time.time() + (ACCESS_TOKEN_EXPIRE_MINUTES * 60) # JWT 토큰 시간
    to_encode.update({"expiry": expire})
    encode_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encode_jwt

def generate_refresh_token(data: dict):
    to_encode = data.copy()
    expire = time.time() + (REFRESH_TOKEN_EXPIRE_DAYS * 43200) # JWT 토큰 시간 30일을 분으로 환산한 값
    to_encode.update({"expiry": expire})
    encode_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encode_jwt

def decodeJWT(token: str): #### JWT 검증을 위한 decoding
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        # print(decode_token["expiry"])
        # print(decode_token["email"])
        # print(time.time())
        return decode_token if decode_token['expiry'] >= time.time() else None
    except:
        return {}

def decode_for_refresh(token: str): #### JWT parsing을 위한 decoding
    decode_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return decode_token