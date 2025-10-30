from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class LinkBase(BaseModel):
    original_url: HttpUrl

class LinkRequest(LinkBase):
    pass

class LinkResponse(LinkBase):
    id: int
    short_code: str
    created_at: datetime
    click_count: int
    user_id: int

    class Config:
        from_attributes = True

class AllLinksResponse(BaseModel):
    links: List[LinkResponse]

class ClickRequest(BaseModel):
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class ClickResponse(BaseModel):
    id: int
    link_id: int
    clicked_at: datetime
    ip_address: Optional[str]
    user_agent: Optional[str]

    class Config:
        from_attributes = True
