from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .civilization_unit import civilization_unit
from .civilization_building import civilization_building
from .civilization_tech import civilization_tech
from .tech import Tech
from .building import Building
from .civilization import Civilization
from .unit import Unit
