from functools import lru_cache

from .jwt_service import JWTService


@lru_cache()
def provide_jwt_service() -> JWTService:
    return JWTService()
