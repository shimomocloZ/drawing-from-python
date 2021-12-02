from migrations.setting import Base
from sqlalchemy import Column, Integer, String


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
