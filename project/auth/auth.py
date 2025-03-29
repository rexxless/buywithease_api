from jose import jwt
import os
from fastapi.responses import JSONResponse
from fastapi import Request
from typing import Callable
from datetime import datetime, timezone, timedelta
from time import time
from dotenv import load_dotenv
from database import cursor, db

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

def create_access_token(data:dict):
    to_encode = {"email":data["email"]}

    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    cursor.execute("SELECT is_admin FROM users WHERE email = %s",(data["email"],))
    to_encode.update({"is_admin": cursor.fetchone()[0], "exp": expire.timestamp()})
    cursor.execute("SELECT id FROM users WHERE email = %s",(data["email"],))
    to_encode.update({"id": cursor.fetchone()[0]})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate(request: Request, next: Callable):
    if request.url.path not in ["/api-shop/product", "/api-shop/cart", "/api-shop/order", "/api-shop/logout"]:
        db.rollback()
        return await next(request)
    else:
        header = request.headers.get("Authorization")
        if not header or not header.startswith("Bearer "):
            return JSONResponse(
                status_code=403,
                content={"message": "Login failed"}
            )
        token = header[7:] 
        cursor.execute("SELECT token FROM invalidtoken")
        decoded = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        if token in [row[0] for row in cursor.fetchall()]:
             cursor.execute(f"DELETE FROM invalidtoken WHERE exp < {datetime.now(timezone.utc).timestamp()}")
             db.commit()
             return JSONResponse(
                status_code=401,
                content={"message": "Token expired"}
             )
        request.state.user = decoded
        if request.url.path in ["/api-shop/product"]:
            try:
                if decoded["is_admin"] is True:
                    return await next(request)
                else:
                    return JSONResponse(
                        status_code=403,
                        content={"message": "Forbidden for you"}
                    )
            except Exception:
                    return JSONResponse(
                        status_code=403,
                        content={"message": "Forbidden for you"}
                    )
        elif request.url.path in ["/api-shop/logout"]:
                return await next(request)
        else:
            try:
                if decoded["is_admin"] is False:
                    return await next(request)
                else:
                    return JSONResponse(
                        status_code=403,
                        content={"message": "Forbidden for you"}
                    )
            except Exception:
                    return JSONResponse(
                        status_code=403,
                        content={"message": "Forbidden for you"}
                    )
