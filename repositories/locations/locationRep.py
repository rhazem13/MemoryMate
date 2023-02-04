# from flask_restful import fields, marshal_with
from math import sin, cos, sqrt, atan2, radians
# from models.db import db
# from models.UserLocations import UserLocationModel
# from sqlalchemy.orm import load_only


R = 6373.0 # Approximate radius of earth in km


class LocationRepo():
 def distance_between_two_points(lat1,lon1,lat2,lon2):
        
        
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return("Distance between the locations given is"+ distance)

def distance_check (lat1,lon1,lat2,lon2,dis):
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        if (dis<distance):
              return("the distance given is less than the right distance")
        if (dis>distance):
              return("the distance given is more than the right distance")
        else:
              return("the distance given matches the right distance")





       
    




    
