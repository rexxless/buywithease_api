from jose import jwt
from fastapi import status, HTTPException, Request, Security, APIRouter
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models import User, NewUser
from auth import SECRET_KEY, ALGORITHM, create_access_token
from database import cursor, db

security = HTTPBearer()
router = APIRouter(prefix="/api-shop", tags=["Users"])


@router.post("/login")
def login(user:User):
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (user.email, user.password))
    user_1 = cursor.fetchone()
    if user_1 is None:
        return JSONResponse(status_code=401, content={"password":"Auth failed"})
    token = create_access_token(data=user.model_dump()) 
    return {"user_token": token}


@router.post("/signup")
def signup(user: NewUser):
    cursor.execute("SELECT * FROM users WHERE email=%s", (user.email,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (fio, email, password) VALUES (%s, %s, %s)", (user.fio, user.email, user.password))
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    token = create_access_token(data=user.model_dump()) 
    cursor.execute("SELECT id FROM users WHERE email=%s", (user.email,))
    user_id = cursor.fetchone()[0]

    cursor.execute(f"""
        CREATE TABLE user_{user_id}_cart (
            id SERIAL PRIMARY KEY,
            product_id INTEGER,
            name TEXT,
            description TEXT,
            price INTEGER
        )
    """)
    db.commit()

    return {"user_token": token}


@router.get("/logout")
def logout(request: Request, credentials: HTTPAuthorizationCredentials = Security(security)):
    decoded = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    exp = decoded["exp"]
    cursor.execute("INSERT INTO invalidtoken (token, exp) VALUES (%s, %s)", (credentials.credentials, exp))
    db.commit()
    return {"message": "Logged out successfully"}