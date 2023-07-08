from sqlalchemy import Table, Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from . import Base

civilization_building = Table(
       'civilization_building', 
       Base.metadata,
       Column('civilization_id', Integer, ForeignKey('civilizations.id')),
       Column('building_id', Integer, ForeignKey('buildings.id'))
  )