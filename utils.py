from datetime import timedelta

from datetime import datetime


#obtain from environment variable in production
secret_key = "fsdfsdfsdfsdflhiugysadf87w940e-=r0werpolwe$16$5*dfsdfsdf&&#$rrr$$)7a9563OO93f7099f6f0f4caa6cf63b88e8d3e7"


#get from environment variable in production
algorithm = "HS256"



def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt



def decode_access_token(*, data: str):
    to_decode = data# import jwt

    return jwt.decode(to_decode, secret_key, algorithm=algorithm)



def generate_hash(length: int):
    import string, random
    uppercase_and_digits = string.ascii_uppercase + string.digits
    gen_hash = ''.join(( random.choice(uppercase_and_digits) for i in range(length)))
    return gen_hash