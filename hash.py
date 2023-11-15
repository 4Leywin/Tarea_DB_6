import bcrypt
import argon2
from argon2 import PasswordHasher
def hash_password_bcrypt(password):
    salt = bcrypt.gensalt(
        rounds=10,
        prefix=b'2a'
    )
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
def hash_password_argon2(password):
    ph = PasswordHasher()
    hashed_password = ph.hash(password)
    return hashed_password
def hash_double(password):
    hash_1 = hash_password_bcrypt(password)
    hash_2 = hash_password_argon2(hash_1)
    return hash_2
def verify_password_bcrypt(entered_password, hashed_password):
    return bcrypt.checkpw(entered_password.encode('utf-8'), hashed_password)