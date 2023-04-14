from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from dsn import DSN

Base = declarative_base()


class Advert(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True)
    heading = Column(String(length=150), nullable=False)
    description = Column(Text, nullable=False)
    owner = Column(String(length=40))
    date_creat = Column(DateTime, server_default=func.now())


engine = create_async_engine(DSN)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)