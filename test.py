import bcrypt
import hashlib
import os

def hash_password_bcrypt(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def hash_password_sha256(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + key

def double_encrypt_password(password):
    # Primer nivel de cifrado: bcrypt
    hashed_password_bcrypt = hash_password_bcrypt(password)

    # Segundo nivel de cifrado: SHA-256
    hashed_password_double = hash_password_sha256(hashed_password_bcrypt.decode('utf-8'))

    return hashed_password_double

def verify_double_encrypted_password(entered_password, hashed_password_double):
    # Verificar en dos etapas: primero con SHA-256, luego con bcrypt
    salt_sha256 = hashed_password_double[:32]
    key_sha256_to_check = hashed_password_double[32:]
    
    hashed_password_bcrypt = hash_password_bcrypt(entered_password)

    key_sha256 = hashlib.pbkdf2_hmac('sha256', hashed_password_bcrypt.decode('utf-8'), salt_sha256, 100000)

    return key_sha256 == key_sha256_to_check

# Ejemplo de uso
password = "my_secure_password"
hashed_password_double = double_encrypt_password(password)

if verify_double_encrypted_password("password_attempt", hashed_password_double):
    print("Contraseña válida (doble cifrado)")
else:
    print("Contraseña incorrecta (doble cifrado)")
