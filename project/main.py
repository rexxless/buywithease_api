from typing import Callable
from jose import ExpiredSignatureError
from fastapi import FastAPI, Request, Security
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from auth import authenticate
from routes import products, cart, orders, users
 
security = HTTPBearer()
app = FastAPI()

@app.middleware("http")
async def authenticate_middleware(request:Request, next: Callable):
    try:
        return await authenticate(request, next)
    except ExpiredSignatureError:
        return JSONResponse(status_code=401, content={"error": "Token expired"})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    custom_errors = {}

    for error in errors:
        field = error["loc"][-1]
        custom_errors[field] = "Validation error"

    return JSONResponse(
        status_code=422,
        content=custom_errors 
    )

app.include_router(users.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)