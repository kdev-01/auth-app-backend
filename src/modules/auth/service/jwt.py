from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from src.core.config import get_settings


class JWTService:
    def __init__(self, settings=None):
        self.settings = settings or get_settings()

    def encode_token(self, user_data: dict) -> str:
        to_encode = user_data.copy()
        expire = datetime.now(timezone.utc) + (
            timedelta(minutes=self.settings.TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.settings.SECRET_KEY, self.settings.ALGORITHM)

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token, self.settings.SECRET_KEY, algorithms=self.settings.ALGORITHM
            )
            if "sub" not in payload:
                raise JWTError("Token inválido: campo 'sub' no encontrado")
            return payload
        except JWTError as e:
            raise JWTError("La sesión ha expirado. Inicie sesión otra vez, por favor.") from e
