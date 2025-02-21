from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import os

db_path = os.path.abspath("qrcodes.db")
DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


class QRCodes(Base):
    __tablename__ = "qrcodes"
    id = Column(Integer, primary_key=True)
    uuid = Column(String(50), unique=True, nullable=False)
    used = Column(Boolean, default=False)


async def init_db():
    """
    Initialize the database.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
