from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Boolean
import os

db_path = os.path.abspath("qrcodes.db")
DATABASE_URL = f"sqlite:///{db_path}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class QRCodes(Base):
    __tablename__ = "qrcodes"
    id = Column(Integer, primary_key=True)
    uuid = Column(String(50), unique=True, nullable=False)
    used = Column(Boolean, default=False)
