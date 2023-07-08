from sqlalchemy import Table, Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from . import Base

class Unit(Base):
    __tablename__ = 'units'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    desc = Column(String(500), nullable=False)
    food_cost = Column(Integer, nullable=True)
    wood_cost = Column(Integer, nullable=True)
    gold_cost = Column(Integer, nullable=True)
    hp = Column(Integer, nullable=False)
    melee_armor = Column(Integer, nullable=True)
    pierce_armor = Column(Integer, nullable=True)
    line_of_sight = Column(Integer, nullable=True)
    range = Column(Integer, nullable=True)
    speed = Column(Float, nullable=True)
    train_time = Column(Integer, nullable=True)
    attack = Column(Integer, nullable=True)
    attack_delay = Column(Float, nullable=True)
    frame_delay = Column(Integer, nullable=True)
    reload_time = Column(Integer, nullable=True)