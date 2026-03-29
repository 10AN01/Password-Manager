from passlib.context import CryptContext
import hashlib
import os
from cryptography.fernet import Fernet
key = os.getenv("ENCRYPTION_KEY").encode() # Gets key from .env file
fernet = Fernet(key)
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)
# Hashes Password
def hash_password(password: str) -> str:
    sha256_hash = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(sha256_hash)

# Verifys password/decrypts to check
def verify_password(plain_password: str, hashed_password: str) -> bool:
    sha256_hash = hashlib.sha256(plain_password.encode()).hexdigest()
    return pwd_context.verify(sha256_hash, hashed_password)


# Use for storing user passwords
def encrypt_password(password: str) -> str:
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password: str) -> str:
    print("ENCRYPTED:", encrypted_password)

    decrypted = fernet.decrypt(encrypted_password.encode()).decode()

    print("DECRYPTED:", decrypted)

    return decrypted