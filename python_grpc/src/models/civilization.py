from sqlalchemy import Table, Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from .civilization_unit import civilization_unit
from .civilization_building import civilization_building
from .civilization_tech import civilization_tech

from . import Base

class Civilization(Base):
    __tablename__ = 'civilizations'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False)
    desc = Column(String(500), nullable=False)
    units = relationship(
        'Unit', secondary=civilization_unit, backref='civilizations')
    buildings = relationship(
        'Building', secondary=civilization_building, backref='civilizations')
    techs = relationship(
        'Tech', secondary=civilization_tech, backref='civilizations')

