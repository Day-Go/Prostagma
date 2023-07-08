import os
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

from ..models import *

class DataAccess:
    def __init__(self, db_filename):
        # get current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # parent directory (src folder)
        parent_dir = os.path.dirname(current_dir)
        
        # construct database path
        db_path = os.path.join(parent_dir, 'data', db_filename)
        
        # connect to the SQLite database
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.metadata = MetaData()
        self.session = self.get_session()

    def get_table(self, table_name):
        # reflect an existing table called table_name from the database
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        return table

    def get_session(self):
        # get a new Session object to interact with the database
        Session = sessionmaker(bind=self.engine)
        return Session()
    
    def get_civ_description(self, civ: str):
        session = self.get_session()
        return session.query(Civilization).where(
            Civilization.name == civ).first().desc
    
    def check_unit_availability(self, civ: str, unit: str):
        session = self.get_session()

        id = session.query(Civilization).where(
                Civilization.name == civ).first().id
        
        unit_id = session.query(Unit).where(
                Unit.name == unit).first().id

        # Check whether the join table, civilization_unit, contains a row
        # with the given civilization and unit ids
        result = session.query(civilization_unit).where(
                        civilization_unit.c.civilization_id == id).where(
                        civilization_unit.c.unit_id == unit_id).count() > 0

        return str(result)
