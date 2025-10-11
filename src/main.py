from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

# DB engine (Close pool in shutdown)
from src.core.database.engine import get_engine
from src.core.middlewares.middleware import AuthMiddleware

# Responses config
from src.core.responses.custom_exceptions import AppException
from src.core.responses.exceptions import (
    app_exception_handler,
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)

# Protected routes
from src.modules.auth.api.routers import router as auth_router
from src.modules.institutions.api.routers import router as institution_router
from src.modules.locations.api.routers import router as city_router
from src.modules.sports.api.routes import router as sport_router
from src.modules.users.api.routers import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    engine = get_engine()
    await engine.dispose()

app = FastAPI(title="Backend FDPEN", lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "Hola Mundo :)"}

# Security settings
app.add_middleware(AuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Standard configuration for endpoint responses
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(AppException, app_exception_handler)

# Routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(institution_router, prefix="/institutions", tags=["Educational Institutions"])
app.include_router(city_router, prefix="/cities", tags=["Cities"])
app.include_router(sport_router, prefix="/sports", tags=["Sports"])
app.include_router(user_router, prefix="/users", tags=["Users"])
