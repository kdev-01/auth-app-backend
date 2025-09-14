from uuid import UUID

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from jose import JWTError
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.responses.helpers import error_response
from src.core.security.jwt_service import JWTService


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        if request.method == "OPTIONS":
            return await call_next(request)
        
        PUBLIC_PATHS = ["/auth/login", "/docs", "/openapi.json"]
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        token = request.cookies.get("access_token")
        if not token:
            return error_response(
                message="Por favor, inicie sesión.",
                status_code=status.HTTP_401_UNAUTHORIZED,
                code="UNAUTHORIZED",
            )
            
        try:
            jwt = JWTService()
            payload = jwt.decode_token(token)
            request.state.user_id = UUID(payload.get("sub"))
            request.state.role = payload.get("role")
            request.state.permissions = payload.get("permissions", [])
            return await call_next(request)
        except JWTError as e:
            return error_response(
                message=str(e),
                status_code=status.HTTP_401_UNAUTHORIZED,
                code="INVALID_TOKEN"
            )
        except Exception as e:
            return error_response(
                message=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                code="AUTH_MIDDLEWARE_ERROR",
            )
