from passlib.context import CryptContext



pwd_contex = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashing(password:str):
    return pwd_contex.hash(password)

def verifying(plain_password, hashed_password):
    return pwd_contex.verify(plain_password, hashed_password)
