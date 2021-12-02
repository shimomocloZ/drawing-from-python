from migrations.setting import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey


class Buyers(Base):
    __tablename__ = 'buyers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    wishlist_id = Column(Integer, ForeignKey('wishlists.id'))
    wishlist = relationship("Wishlists")
