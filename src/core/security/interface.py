from typing import Protocol


class IJWTService(Protocol):
    def encode_token(self, payload: dict, expires_in_minutes: int) -> str: ...
    def decode_token(self, token: str) -> dict: ...
    