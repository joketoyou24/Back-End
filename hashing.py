from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password : str):
        return pwd_context.hash(password)
    
    def verify(hashed_password, password):
        return pwd_context.verify(password,hashed_password)