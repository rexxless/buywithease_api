from jose import jwt
from fastapi import Request, Security, APIRouter
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from auth import SECRET_KEY, ALGORITHM
from database import cursor, db

security = HTTPBearer()
router = APIRouter(prefix="/api-shop", tags=["Cart"])

@router.get("/cart")
def cart(request: Request, credentials: HTTPAuthorizationCredentials = Security(security)):
    payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    user_email = payload.get("email")
    cursor.execute("SELECT id FROM users WHERE email = %s", (user_email,))
    user_id = cursor.fetchone()

    user_id = user_id[0] 

    cursor.execute(f"SELECT * FROM user_{user_id}_cart")
    cart_items = cursor.fetchall()
    data = [{"id": row[0], "product_id": row[1], "name": row[2], "description": row[3], "price": row[4]}for row in cart_items]

    return data

@router.post("/cart/{product_id}")
def add_to_cart(product_id: int, request: Request, credentials: HTTPAuthorizationCredentials = Security(security)):
    payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    user_email = payload.get("email")

    cursor.execute("SELECT id FROM users WHERE email = %s", (user_email,))
    user_id = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    
    if not product:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    
    cart = f"user_{user_id}_cart"
    cursor.execute(f"INSERT INTO {cart}(product_id, name, description, price) VALUES (%s, %s, %s, %s)",(product[0], product[1], product[2], product[3])) 
    db.commit()
    return {"message": "Product add to cart"}

@router.delete("/cart/{cart_product_id}")
def remove_from_cart(cart_product_id: int, request: Request, credentials: HTTPAuthorizationCredentials = Security(security)):
    payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    user_email = payload.get("email")
    cursor.execute("SELECT id FROM users WHERE email = %s", (user_email,))
    user_id = cursor.fetchone()[0]
    cart = f"user_{user_id}_cart"

    cursor.execute(f"SELECT * FROM {cart} WHERE id = %s", (cart_product_id,))
    product = cursor.fetchone()
    if not product:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    
    cursor.execute(f"DELETE FROM {cart} WHERE id = %s", (cart_product_id,))
    
    cursor.execute(f"""
        UPDATE {cart}
        SET id = new_id
        FROM (
            SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS new_id
            FROM {cart}
        ) AS numbered
        WHERE {cart}.id = numbered.id;
    """)
    cursor.execute(f"SELECT MAX(id) FROM {cart}")
    max_id = cursor.fetchone()[0] or 0 
    cursor.execute(f"ALTER SEQUENCE {cart}_id_seq RESTART WITH {max_id + 1}")
    
    db.commit()
    return {"message": "Item removed from cart"}