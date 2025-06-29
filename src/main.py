from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

# Responses config
from src.core.responses.exceptions import (
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)

# Routes
from src.modules.auth.router import router as auth_router
from src.modules.users.router import router as users_router

from .middleware import AuthMiddleware

app = FastAPI(title="Backend FDPEN")

# Standard configuration for endpoint responses
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Security settings
app.add_middleware(AuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["User"])
