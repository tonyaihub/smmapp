from sqlalchemy import String, Integer, DateTime, func, Enum
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
import enum

class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    PRO = "pro"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)
    subscription_tier: Mapped[SubscriptionTier] = mapped_column(Enum(SubscriptionTier), default=SubscriptionTier.FREE)
    stripe_customer_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(server_default=func.now())

class GenerationHistory(Base):
    __tablename__ = "generations"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    topic: Mapped[str] = mapped_column(String(512))
    created_at: Mapped[DateTime] = mapped_column(server_default=func.now())
