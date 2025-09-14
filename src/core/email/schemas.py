from typing import List, Optional

from pydantic import BaseModel, EmailStr


class EmailMessage(BaseModel):
    subject: str
    body: str
    to: List[EmailStr]
    from_email: EmailStr
    html: Optional[bool] = False
