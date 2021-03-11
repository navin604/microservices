from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class AutoPilot(Base):
    """ Auto Pilot """

    __tablename__ = "auto_pilot"

    id = Column(Integer, primary_key=True)
    vehicle_id = Column(String(250), nullable=False)
    time = Column(String(250), nullable=False)
    location = Column(String(100), nullable=False)
    speed_at_enable = Column(Integer, nullable=False)
    weather_data = Column(String(250), nullable=False)
    follow_distance = Column(String(100), nullable=False)
    highway = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)



    def __init__(self, vehicle_id, time, location, speed_at_enable, highway, weather_data, follow_distance):
        """ Initializes a auto pilot reading """




        self.vehicle_id = vehicle_id
        self.time = time
        self.location = location
        self.date_created = datetime.datetime.now() # Sets the date/time record is created
        self.weather_data = weather_data
        self.follow_distance = follow_distance
        self.highway = highway
        self.speed_at_enable = speed_at_enable

    def to_dict(self):
        """ Dictionary Representation of an auto pilot reading """
        dict = {}
        dict['id'] = self.id
        dict['vehicle_id'] = self.vehicle_id
        dict['time'] = self.time
        dict['location'] = self.location
        dict['date_created'] = self.date_created
        dict['weather_data'] = self.weather_data
        dict['follow_distance'] = self.follow_distance
        dict['highway'] = self.highway
        dict['speed_at_enable'] = self.speed_at_enable

        return dict
