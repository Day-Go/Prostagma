import os
import re
import json
from pprint import PrettyPrinter
from bs4 import BeautifulSoup

from sqlalchemy import Table, Column, Integer, Float, ForeignKey, String, create_engine, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
pp = PrettyPrinter(indent=4)


class CivilizationUnit(Base):
    __tablename__ = 'civilization_unit'
    civilization_id = Column(Integer, ForeignKey(
        'civilizations.id'), primary_key=True)
    unit_id = Column(Integer, ForeignKey('units.id'), primary_key=True)
    __table_args__ = (
        Index('ix_civilization_unit_civilization_id', 'civilization_id'),
        Index('ix_civilization_unit_unit_id', 'unit_id'),
    )


class CivilizationBuilding(Base):
    __tablename__ = 'civilization_building'
    civilization_id = Column(Integer, ForeignKey(
        'civilizations.id'), primary_key=True)
    building_id = Column(Integer, ForeignKey('buildings.id'), primary_key=True)
    __table_args__ = (
        Index('ix_civilization_building_civilization_id', 'civilization_id'),
        Index('ix_civilization_building_building_id', 'building_id'),
    )


class CivilizationTech(Base):
    __tablename__ = 'civilization_tech'
    civilization_id = Column(Integer, ForeignKey(
        'civilizations.id'), primary_key=True)
    tech_id = Column(Integer, ForeignKey('techs.id'), primary_key=True)
    __table_args__ = (
        Index('ix_civilization_tech_civilization_id', 'civilization_id'),
        Index('ix_civilization_tech_tech_id', 'tech_id'),
    )


class Civilization(Base):
    __tablename__ = 'civilizations'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False)
    bonuses = Column(String(250), nullable=False)
    unique_units = Column(String(250), nullable=False)
    unique_techs = Column(String(250), nullable=False)
    team_bonus = Column(String(250), nullable=False)
    units = relationship(
        'Unit', secondary='civilization_unit', backref='civilizations')
    buildings = relationship(
        'Building', secondary='civilization_building', backref='civilizations')
    techs = relationship(
        'Tech', secondary='civilization_tech', backref='civilizations')
    __table_args__ = (
        Index('ix_civilizations_name', 'name'),
    )


class Building(Base):
    __tablename__ = 'buildings'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    desc = Column(String(500), nullable=False)
    __table_args__ = (
        Index('ix_buildings_name', 'name'),
    )


class Tech(Base):
    __tablename__ = 'techs'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    desc = Column(String(500), nullable=False)
    __table_args__ = (
        Index('ix_techs_name', 'name'),
    )


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
    __table_args__ = (
        Index('ix_units_name', 'name'),
    )

# Extract civilization attributes from the description string


def extract_civ_attributes(desc):
    # Split the description string into sections based on the specified delimiters
    sections = re.split(
        r" Unique Unit[s]*: | Unique Tech[s]*: | Team Bonus: ", desc)

    # Assign each section to the corresponding attribute, or None if the section is not present
    bonuses = sections[0].strip() if len(sections) > 0 else None
    unique_units = sections[1].strip() if len(sections) > 1 else None
    unique_techs = sections[2].strip() if len(sections) > 2 else None
    team_bonus = sections[3].strip() if len(sections) > 3 else None

    return bonuses, unique_units, unique_techs, team_bonus


if __name__ == '__main__':
    db_path = './example.db'

    # Check if the file exists
    if os.path.exists(db_path):
        # Delete the database file
        os.remove(db_path)

    # Create the engine
    # Use SQLite for the example
    engine = create_engine('sqlite:///example.db')

    # Set up the session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create the database
    Base.metadata.create_all(engine)

    def extract_unit_name(desc):
        match = re.search(r'<b>(.*?)</b>', desc)
        if match:
            extracted_string = match.group(1)
            return extracted_string

    def extract_unit_description(desc):
        desc = desc.split('\n')[1]
        soup = BeautifulSoup(desc, 'html.parser')
        clean_string = soup.get_text()
        return clean_string

    # Get the directory of the script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to data.json
    data_file_path = os.path.join(script_dir, 'data.json')
    string_file_path = os.path.join(script_dir, 'strings.json')

    with open(data_file_path, 'r') as tech_tree:
        with open(string_file_path, 'rb') as descriptions:

            contents = json.load(tech_tree)
            descs = json.load(descriptions)
            units = contents["data"]["units"]
            buildings = contents["data"]["buildings"]
            techs = contents["data"]["techs"]
            bonuses = contents["civ_helptexts"]
            civilizations = contents["techtrees"]

            for id, data in units.items():
                unit_name = extract_unit_name(
                    descs[f"{data['LanguageHelpId']}"])
                unit_description = extract_unit_description(
                    descs[f"{data['LanguageHelpId']}"])

                food_cost = data["Cost"].get("Food", 0)
                wood_cost = data["Cost"].get("Wood", 0)
                gold_cost = data["Cost"].get("Gold", 0)

                hp = data["HP"]
                melee_armor = data["MeleeArmor"]
                pierce_armor = data["PierceArmor"]
                line_of_sight = data["LineOfSight"]
                range = data["Range"]
                speed = data["Speed"]
                train_time = data["TrainTime"]
                attack = data["Attack"]
                attack_delay = data["AttackDelaySeconds"]
                frame_delay = data["FrameDelay"]
                reload_time = data["ReloadTime"]

                # load all values into the unit class
                unit = Unit(id=id, name=unit_name, desc=unit_description, food_cost=food_cost,
                            wood_cost=wood_cost, gold_cost=gold_cost, hp=hp, melee_armor=melee_armor,
                            pierce_armor=pierce_armor, line_of_sight=line_of_sight, range=range,
                            speed=speed, train_time=train_time, attack=attack, attack_delay=attack_delay,
                            frame_delay=frame_delay, reload_time=reload_time)

                session.add(unit)

            for id, data in buildings.items():
                unit_name = extract_unit_name(
                    descs[f"{data['LanguageHelpId']}"])
                unit_description = extract_unit_description(
                    descs[f"{data['LanguageHelpId']}"])

                building = Building(id=id, name=unit_name,
                                    desc=unit_description)

                session.add(building)

            for id, data in techs.items():

                match = re.search(
                    r'<b>(.*?)</b>', descs[f"{data['LanguageHelpId']}"])
                if match:
                    name = match.group(1)

                desc = descs[f"{data['LanguageHelpId']}"].split('\n')[1]

                tech = Tech(id=id, name=name, desc=desc)

                session.add(tech)

            session.commit()

            for id, ((name, data), relations) in enumerate(zip(bonuses.items(), civilizations.values())):

                t = descs[f"{data}"].split('\n')[0]
                soup = BeautifulSoup(t, 'html.parser')
                clean_t = soup.get_text()
                clean_t = clean_t.replace(' civilization', '')

                desc = ' '.join(descs[f"{data}"].split('\n')[2:])
                soup = BeautifulSoup(desc, 'html.parser')
                clean_desc = soup.get_text()

                # Extract the civilization attributes from the description string
                bonuses, unique_units, unique_techs, team_bonus = extract_civ_attributes(
                    clean_desc)

                civilization = Civilization(
                    id=id,
                    name=name,
                    type=clean_t,
                    bonuses=bonuses,
                    unique_units=unique_units,
                    unique_techs=unique_techs,
                    team_bonus=team_bonus,
                )

                # civilization = Civilization(
                #     id=id, name=name, type=clean_t, desc=clean_desc)

                for b in relations['buildings']:
                    building = session.query(Building).filter_by(id=b).first()
                    building.civilizations.append(civilization)

                for u in relations['units']:
                    unit = session.query(Unit).filter_by(id=u).first()
                    unit.civilizations.append(civilization)

                for t in relations['techs']:
                    tech = session.query(Tech).filter_by(id=t).first()
                    tech.civilizations.append(civilization)

                for name, unique in relations['unique'].items():
                    if 'Unit' in name:
                        unit = session.query(Unit).filter_by(id=unique).first()
                        unit.civilizations.append(civilization)
                    elif 'Tech' in name:
                        tech = session.query(Tech).filter_by(id=unique).first()
                        tech.civilizations.append(civilization)

                session.add(civilization)

    session.commit()

    # Query the database
    b = session.query(Civilization).where(
        Civilization.name == 'Aztecs').first().buildings

    for j in b:
        print(j.name)

    # get all units available to the Britons
    b = session.query(Civilization).where(
        Civilization.name == 'Britons').first().units

    for j in b:
        print(j.name)
