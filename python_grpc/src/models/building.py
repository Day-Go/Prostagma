from sqlalchemy import Table, Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from . import Base

class Building(Base):
    __tablename__ = 'buildings'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    desc = Column(String(500), nullable=False)

