from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class AutoBrake(Base):
    """ Auto Brake """

    __tablename__ = "auto_brake"

    id = Column(Integer, primary_key=True)
    vehicle_id = Column(String(250), nullable=False)
    time = Column(String(250), nullable=False)
    location = Column(String(100), nullable=False)
    speed_at_enable = Column(Integer, nullable=False)
    weather_data = Column(String(250), nullable=False)
    follow_distance = Column(String(100), nullable=False)
    highway = Column(Integer, nullable=False)
    engaged = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)



    def __init__(self, time, location, speed_at_enable, highway, weather_data, follow_distance, vehicle_id, engaged):
        """ Initializes an auto brake reading """

        self.vehicle_id = vehicle_id
        self.time = time
        self.engaged = engaged
        self.location = location
        self.date_created = datetime.datetime.now()
        self.weather_data = weather_data
        self.follow_distance = follow_distance
        self.highway = highway
        self.speed_at_enable = speed_at_enable

    def to_dict(self):
        """ Dictionary Representation of an auto brake reading """
        dict = {}
        dict['id'] = self.id
        dict['vehicle_id'] = self.vehicle_id
        dict['time'] = self.time
        dict['location'] = self.location
        dict['date_created'] = self.date_created
        dict['weather_data'] = self.weather_data
        dict['follow_distance'] = self.follow_distance
        dict['highway'] = self.highway
        dict['engaged'] = self.engaged
        dict['speed_at_enable'] = self.speed_at_enable

        return dict
