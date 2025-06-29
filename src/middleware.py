from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from jose import JWTError
from starlette.middleware.base import BaseHTTPMiddleware

from .core.responses.helpers import error_response
from .modules.auth.service.jwt import JWTService


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        PUBLIC_PATHS = ["/auth/login", "/docs", "/openapi.json"]

        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        token = request.cookies.get("access_token")
        if not token:
            return error_response(
                errors=[{"msg": "Por favor, inicie sesión."}],
                message="Unauthorized",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
            
        try:
            jwt = JWTService()
            payload = jwt.decode_token(token)
            request.state.user_id = payload.get("sub")
            request.state.user_role = payload.get("role")
            return await call_next(request)
        except JWTError as e:
            return error_response(
                errors=[{"msg": str(e)}],
                message="Unauthorized",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        except Exception:
            return error_response(
                errors=[{"msg": "Error interno del servidor"}],
                message="Internal Server Error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
