from fastapi import Request, Security, APIRouter
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models import Product, ProductUpdate
from database import cursor, db

security = HTTPBearer()
router = APIRouter(prefix="/api-shop", tags=["Products"])

@router.get("/products")
def read_root():
    cursor.execute("SELECT * FROM products ORDER BY id")
    data = [{"id": row[0], "name": row[1], "description":row[2], "price": row[3]} for row in cursor.fetchall()]
    return data


# -------------------------------------------- Admin Only -------------------------------------------
@router.post("/product")
def create_product(product:Product, request: Request, credentials: HTTPAuthorizationCredentials = Security(security)):
    cursor.execute("INSERT INTO products (name, description, price) VALUES (%s, %s, %s)", (product.name, product.description, product.price))
    db.commit()
    cursor.execute("SELECT * FROM products OFFSET ((SELECT COUNT(*) from PRODUCTS)-1)")
    return {"id": cursor.fetchone()[0] , "message": "Product added"}

@router.delete("/product/{product_id}")
def delete_product(product_id: int, request: Request, credentials: HTTPAuthorizationCredentials = Security(security)):
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    
    if not product:
        return JSONResponse(status_code=404,
                            content={"message":"Not found"})
    
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    db.commit()

    return {"message": "Product deleted successfully"}

@router.patch("/product/{product_id}")
def update_product(product_id: int, product_update: ProductUpdate, request: Request, credentials: HTTPAuthorizationCredentials = Security(security)):
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    existing_product = cursor.fetchone()
    if not existing_product:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    
    update_fields = []
    update_values = []
    
    if product_update.name is not None:
        update_fields.append("name = %s")
        update_values.append(product_update.name)
    
    if product_update.description is not None:
        update_fields.append("description = %s")
        update_values.append(product_update.description)

    if product_update.price is not None:
        update_fields.append("price = %s")
        update_values.append(product_update.price)

    if not update_fields:
        return existing_product
    
    update_values.append(product_id)
    update_query = f"UPDATE products SET {', '.join(update_fields)} WHERE id = %s"
    cursor.execute(update_query, update_values)
    db.commit()
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    data = {"id": product[0], "name": product[1], "description":product[2], "price": product[3]}
    return data

