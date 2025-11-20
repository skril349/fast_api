# XXXXXX.YYYYYYY.ZZZZZZZ
# text codificat en 3 parts
import jwt 
import datetime


SECRET_KEY = "99841f84c2055e0f75249901d6cd9639"
ALGORITHM = "HS256"

payload :dict = {
    "username":"Eduardo Rios",
    "role":"admin",
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours = 1)
}

# Crear el token
token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Verificar/decodificar el token

try:
    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print("Decoded payload:", decoded_payload)
except jwt.ExpiredSignatureError:
    print("Token has expired")
except jwt.InvalidTokenError:
    print("Invalid token")