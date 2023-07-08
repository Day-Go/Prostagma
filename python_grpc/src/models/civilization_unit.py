from sqlalchemy import Table, Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from . import Base

civilization_unit = Table(
       'civilization_unit', 
       Base.metadata,
       Column('civilization_id', Integer, ForeignKey('civilizations.id')),
       Column('unit_id', Integer, ForeignKey('units.id'))
)