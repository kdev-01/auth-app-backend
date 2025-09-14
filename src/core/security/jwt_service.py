from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from src.core.config import get_settings
from src.core.timezone import ECUADOR_TZ


class JWTService:
    def __init__(self, settings=None):
        self.settings = settings or get_settings()

    def encode_token(self, payload: dict, expires_in_minutes: int = 1440) -> str:
        to_encode = payload.copy()
        expire = datetime.now(ECUADOR_TZ) + timedelta(minutes=expires_in_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.settings.SECRET_KEY, self.settings.ALGORITHM)

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                self.settings.SECRET_KEY,
                algorithms=[self.settings.ALGORITHM]
            )
            return payload
        except JWTError as e:
            raise JWTError("La sesión ha expirado.") from e
