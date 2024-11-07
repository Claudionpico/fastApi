import jwt

def createToken(data: dict):
    token: str = jwt.encode(payload=data, key='secret', algorithm="HS256") # key is entorno variable
    return token

def verifyToken(token: str):
    try:
        data = jwt.decode(token, 'secret', algorithms=["HS256"])
        return data
    except:
        return "Invalid token"