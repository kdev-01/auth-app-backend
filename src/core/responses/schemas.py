from typing import List, Optional

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    msg: str
    loc: Optional[List[str]] = None
    type: Optional[str] = None
