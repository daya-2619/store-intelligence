from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Float,
    BigInteger,
    DateTime,
    Integer,
    Index,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import JSONB


class Base(DeclarativeBase):
    pass


class Event(Base):

    __tablename__ = "events"

    event_id = Column(
        String,
        primary_key=True
    )

    store_id = Column(String, index=True)

    camera_id = Column(String, index=True)

    visitor_id = Column(String, index=True)

    event_type = Column(String, index=True)

    zone_id = Column(String)

    timestamp = Column(
        DateTime(timezone=True),
        index=True
    )

    dwell_ms = Column(
        BigInteger
    )

    is_staff = Column(
        Boolean
    )

    confidence = Column(
        Float
    )

    event_metadata = Column(
        JSONB
    )

    __table_args__ = (
        Index("ix_events_store_time_staff", "store_id", "timestamp", "is_staff"),
    )


class VisitorSession(Base):

    __tablename__ = "visitor_sessions"

    visitor_id = Column(
        String,
        primary_key=True
    )

    store_id = Column(
        String,
        primary_key=True,
        index=True
    )

    entry_time = Column(
        DateTime(timezone=True)
    )

    exit_time = Column(
        DateTime(timezone=True)
    )

    converted = Column(
        Boolean,
        default=False
    )

    is_staff = Column(
        Boolean,
        default=False
    )


class POSTransaction(Base):

    __tablename__ = "pos_transactions"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    store_id = Column(String, index=True)
    
    transaction_id = Column(String, unique=True, index=True)

    timestamp = Column(
        DateTime(timezone=True),
        index=True
    )

    basket_value_inr = Column(Float)


class BillingVisit(Base):

    __tablename__ = "billing_visits"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    visitor_id = Column(
        String,
        nullable=False
    )

    store_id = Column(
        String,
        nullable=False,
        index=True
    )

    billing_enter_time = Column(
        DateTime(timezone=True)
    )

class Store(Base):

    __tablename__ = "stores"

    store_id = Column(
        String,
        primary_key=True
    )

    store_name = Column(String, nullable=False)
    city = Column(String)
    region = Column(String)
    active = Column(Boolean, default=True)
    layout_path = Column(String)


class StoreLayout(Base):

    __tablename__ = "store_layouts"

    id = Column(
        Integer,
        primary_key=True
    )

    store_id = Column(
        String,
        ForeignKey("stores.store_id")
    )

    layout_path = Column(String)

    width = Column(Integer)
    height = Column(Integer)


class Camera(Base):

    __tablename__ = "cameras"

    camera_id = Column(
        String,
        primary_key=True
    )

    store_id = Column(String, ForeignKey("stores.store_id"), index=True, nullable=False)
    
    camera_name = Column(String)
    camera_type = Column(String)
    zone_name = Column(String)
    is_heatmap_enabled = Column(Boolean, default=True)

    status = Column(String, default="ONLINE")
    
    stream_url = Column(String)
    source_path = Column(String)