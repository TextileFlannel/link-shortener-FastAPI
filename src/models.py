from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from src.database import base as Base
from sqlalchemy.orm import relationship

class Link(Base):
    __tablename__ = 'links'

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(Text, nullable=False)
    short_code = Column(String(10), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    click_count = Column(Integer, default=0)

    clicks = relationship("Click", back_populates="link", cascade="all, delete-orphan")

class Click(Base):
    __tablename__ = 'clicks'

    id = Column(Integer, primary_key=True, index=True)
    link_id = Column(Integer, ForeignKey("links.id", ondelete="CASCADE"), nullable=False)
    clicked_at = Column(DateTime(timezone=True), server_default=func.now())
    ip_address = Column(String(45))
    user_agent = Column(Text)

    link = relationship("Link", back_populates="clicks")