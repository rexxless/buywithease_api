from jose import jwt
from fastapi import Request, Security, APIRouter
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from auth import SECRET_KEY, ALGORITHM
from database import cursor, db

security = HTTPBearer()
router = APIRouter(prefix="/api-shop", tags=["Orders"])

@router.post("/order")
def create_order(request: Request, credentials: HTTPAuthorizationCredentials = Security(security)):
    payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    user_email = payload.get("email")
    
    cursor.execute("SELECT id FROM users WHERE email = %s", (user_email,))
    user_id = cursor.fetchone()[0]
    
    cart = f"user_{user_id}_cart"
    cursor.execute(f"SELECT * FROM {cart}")
    cart_items = cursor.fetchall()
    
    if not cart_items:
        return JSONResponse(
            status_code=422, 
            content={"error": {"code": 422, "message": "Cart is empty"}}
        )
    
    products = [item[1] for item in cart_items] 
    order_price = sum(item[4] for item in cart_items) 
    
    cursor.execute(
        "INSERT INTO orders (user_id, products, order_price) VALUES (%s, %s, %s) RETURNING id",
        (user_id, products, order_price)
    )
    order_id = cursor.fetchone()[0]
    db.commit()
    
    cursor.execute(f"DELETE FROM {cart}")
    db.commit()
    
    return {"order_id": order_id, "message": "Order created successfully"}

@router.get("/order")
def orders(request:Request, credentials: HTTPAuthorizationCredentials = Security(security)):
    payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    user_email = payload.get("email")

    cursor.execute("SELECT id FROM users WHERE email = %s", (user_email,))
    user_id = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM orders WHERE user_id = %s ORDER BY id", (user_id,))
    orders = cursor.fetchall()
    return [{"id": row[0], "products": row[2], "order_price": row[3]} for row in orders]