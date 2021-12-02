from migrations.setting import Base
from sqlalchemy import Column, Integer, String


class Wishlists(Base):
    __tablename__ = 'wishlists'

    id = Column(Integer, primary_key=True, autoincrement=True)
    priority = Column(String(1000), nullable=False)
    number_of_buy = Column(String(1000), nullable=False)
