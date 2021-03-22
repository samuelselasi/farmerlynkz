# from datetime import datetime, timedelta
# import string, random, jwt, sys, shutil
# from exceptions import FileReadFailed
# from typing import Optional
# from main import settings
# import pandas as pd

# uppercase_and_digits = string.ascii_uppercase + string.digits
# lowercase_and_digits = string.ascii_lowercase + string.digits

# def gen_alphanumeric_code(length):
#     code = ''.join((random.choice(uppercase_and_digits) for i in range(length)))
#     return code

# def create_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=30)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
#     return encoded_jwt

# def decode_token(*, data: str):
#     to_decode = data
#     return jwt.decode(to_decode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# async def read_xcl_file_contents(file, header):
#     file = await file.read()
#     try:
#         return pd.read_excel(file, names=header)
#     except ValueError:
#         raise ValueError
#     except:
#         raise FileReadFailed('{}'.format(sys.exc_info()[0]))

# async def read_csv_file_contents(file, header):
#     file = await file.read()
#     try:
#         return pd.read_excel(file, names=header)
#     except ValueError:
#         raise ValueError
#     except:
#         raise FileReadFailed()

# def logical_xor(a, b):
#     return bool(a) ^ bool(b)

# def get_list_pairs(list1, list2, index:int=0):
#     combination = []
#     for i1 in list1:
#         for i2 in list2:
#             combination.append((i1,i2, str(gen_2_pow_n(index))))
#             index+=1
#     return combination

# def gen_2_pow_n(pow):
#     return 2**pow

# def timestamp_to_datetime(timestamp):
#     dt_obj = datetime.fromtimestamp(timestamp)
#     return dt_obj