from sqlalchemy import Table, Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from . import Base

civilization_tech = Table(
       'civilization_tech', 
       Base.metadata,
       Column('civilization_id', Integer, ForeignKey('civilizations.id')),
       Column('tech_id', Integer, ForeignKey('techs.id'))
)
