"""Objects representing a database and database objects for storing health data from Oura."""

__author__ = "Tom Goetz"
__copyright__ = "Copyright Tom Goetz"
__license__ = "GPL"

import logging
from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Boolean, JSON, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

import idbutils

logger = logging.getLogger(__name__)

OuraDb = idbutils.DB.create('oura', 1, "Database for storing health data from Oura.")


class Profile(OuraDb.Base, idbutils.DbObject):
    """Class representing Oura user profile."""
    __tablename__ = 'profile'
    db = OuraDb
    table_version = 1

    id = Column(String, primary_key=True)
    email = Column(String)
    weight = Column(Float)
    height = Column(Float)
    age = Column(Integer)
    biological_sex = Column(String)


class DailySleep(OuraDb.Base, idbutils.DbObject):
    """Class representing Oura daily sleep data."""
    __tablename__ = 'daily_sleep'
    db = OuraDb
    table_version = 1

    day = Column(Date, primary_key=True)
    score = Column(Integer)
    contributors = Column(JSON)
    id = Column(String)
    timestamp = Column(DateTime)
    
    # Flattened key metrics could go here but JSON is flexible for now
    # We can expand this based on precise needs later


class DailyActivity(OuraDb.Base, idbutils.DbObject):
    """Class representing Oura daily activity data."""
    __tablename__ = 'daily_activity'
    db = OuraDb
    table_version = 1

    day = Column(Date, primary_key=True)
    score = Column(Integer)
    active_calories = Column(Integer)
    average_met = Column(Float)
    contributers = Column(JSON)
    equivalent_walking_distance = Column(Integer)
    high_activity_met_min = Column(Integer)
    high_activity_time = Column(Integer)
    inactivity_alerts = Column(Integer)
    low_activity_met_min = Column(Integer)
    low_activity_time = Column(Integer)
    medium_activity_met_min = Column(Integer)
    medium_activity_time = Column(Integer)
    met = Column(JSON)
    meters_to_target = Column(Integer)
    non_wear_time = Column(Integer)
    resting_time = Column(Integer)
    sedentary_met_min = Column(Integer)
    sedentary_time = Column(Integer)
    steps = Column(Integer)
    target_calories = Column(Integer)
    target_meters = Column(Integer)
    total_calories = Column(Integer)
    timestamp = Column(DateTime)


class DailyReadiness(OuraDb.Base, idbutils.DbObject):
    """Class representing Oura daily readiness data."""
    __tablename__ = 'daily_readiness'
    db = OuraDb
    table_version = 1

    day = Column(Date, primary_key=True)
    score = Column(Integer)
    contributors = Column(JSON)
    temperature_deviation = Column(Float)
    temperature_trend_deviation = Column(Float)
    timestamp = Column(DateTime)


class HeartRate(OuraDb.Base, idbutils.DbObject):
    """Class representing Oura heart rate data."""
    __tablename__ = 'heartrate'
    db = OuraDb
    table_version = 1

    timestamp = Column(DateTime, primary_key=True)
    bpm = Column(Integer)
    source = Column(String)


class Session(OuraDb.Base, idbutils.DbObject):
    """Class representing Oura sessions (workouts/meditations)."""
    __tablename__ = 'sessions'
    db = OuraDb
    table_version = 1

    id = Column(String, primary_key=True)
    day = Column(Date)
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    type = Column(String)
    mood = Column(String)
    motion_count = Column(JSON)


class Workout(OuraDb.Base, idbutils.DbObject):
    """Class representing Oura workouts."""
    __tablename__ = 'workouts'
    db = OuraDb
    table_version = 1

    id = Column(String, primary_key=True)
    day = Column(Date)
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    activity = Column(String)
    calories = Column(Float)
    distance = Column(Float)
    
  
class Tag(OuraDb.Base, idbutils.DbObject):
    """Class representing Oura tags."""
    __tablename__ = 'tags'
    db = OuraDb
    table_version = 1

    id = Column(String, primary_key=True)
    # Tags often have a timestamp and text/type
    day = Column(Date)
    text = Column(String)
    timestamp = Column(DateTime)
    tags = Column(JSON)


class SpO2(OuraDb.Base, idbutils.DbObject):
    """Class representing Oura SpO2 data."""
    __tablename__ = 'spo2'
    db = OuraDb
    table_version = 1

    day = Column(Date, primary_key=True)
    average = Column(Float)


class Stress(OuraDb.Base, idbutils.DbObject):
    """Class representing Oura stress data."""
    __tablename__ = 'stress'
    db = OuraDb
    table_version = 1

    day = Column(Date, primary_key=True)
    stress_high = Column(Integer)
    recovery_high = Column(Integer)
    day_summary = Column(JSON)


class RingConfiguration(OuraDb.Base, idbutils.DbObject):
    """Class representing Oura ring configuration."""
    __tablename__ = 'ring_configuration'
    db = OuraDb
    table_version = 1

    id = Column(String, primary_key=True)
    color = Column(String)
    design = Column(String)
    firmware_version = Column(String)
    hardware_type = Column(String)
    model = Column(String)
    size = Column(Integer)


class HeartHealth(OuraDb.Base, idbutils.DbObject):
    """Class representing Oura Heart Health (Cardiovascular Age, etc)."""
    __tablename__ = 'heart_health'
    db = OuraDb
    table_version = 1

    day = Column(Date, primary_key=True)
    vascular_age = Column(Integer)
    
