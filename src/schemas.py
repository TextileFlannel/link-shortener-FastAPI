from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class LinkBase(BaseModel):
    original_url: str

class LinkRequest(LinkBase):
    pass

class LinkResponse(LinkBase):
    id: int
    short_code: str
    created_at: datetime
    click_count: int

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