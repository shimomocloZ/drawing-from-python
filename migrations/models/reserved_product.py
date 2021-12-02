from migrations.setting import Base
from sqlalchemy import Column, Integer, String


class ReservedProducts(Base):
    __tablename__ = 'reserved_products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(100), nullable=False, unique=True)
    buyer_name = Column(String, nullable=False)
    number_of_buy = Column(Integer, nullable=False)
