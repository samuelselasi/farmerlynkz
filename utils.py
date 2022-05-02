# IMPORT DEENDENCIES
from datetime import datetime, timedelta
import string
import random
import jwt
import sys
from exceptions import FileReadFailed
from typing import Optional
from main import settings
import pandas as pd

# DEFINE CHARACTERS USED IN TOKEN
uppercase_and_digits = string.ascii_uppercase + string.digits
lowercase_and_digits = string.ascii_lowercase + string.digits

# GENERATE ACCESS CODES


def gen_alphanumeric_code(length):
    code = ''.join((random.choice(uppercase_and_digits)
                   for i in range(length)))
    return code

# CREATE ACCESS TOKEN


def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        # DEFINE EXPIRY DATE FOR ACCESS TOKEN
        expire = datetime.utcnow() + expires_delta
    else:
        # EXPIRES 30 MINUTES AFTER CREATION
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    # GET SECRET KEY FOR TOKEN FROM CONFIG.PY
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# DECRYPT ACCESS TOKEN


def decode_token(data: str, key: settings.SECRET_KEY, algorithm: settings.ALGORITHM):
    to_decode = data
    # GET SECRET KEY FOR TOKEN FROM CONFIG.PY
    return jwt.decode(to_decode, key, algorithm)

# GET XCL FILE CONTENTS


async def read_xcl_file_contents(file, header):
    file = await file.read()
    try:
        return pd.read_excel(file, names=header)
    except ValueError:
        raise ValueError
    except FileReadFailed:
        raise FileReadFailed('{}'.format(sys.exc_info()[0]))

# READ CSV FILE CONTENTS


async def read_csv_file_contents(file, header):
    file = await file.read()
    try:
        return pd.read_excel(file, names=header)
    except ValueError:
        raise ValueError
    except FileReadFailed:
        raise FileReadFailed()

# BOOLEAN LOGIC


def logical_xor(a, b):
    return bool(a) ^ bool(b)

# GET PAIR COMBINATIONS FOR ACCESS TOKEN


def get_list_pairs(list1, list2, index: int = 0):
    combination = []
    for i1 in list1:
        for i2 in list2:
            combination.append((i1, i2, str(gen_2_pow_n(index))))
            index += 1
    return combination

# GENERATE POW


def gen_2_pow_n(pow):
    return 2**pow

# TIME-STAMP


def timestamp_to_datetime(timestamp):
    dt_obj = datetime.fromtimestamp(timestamp)
    return dt_obj
