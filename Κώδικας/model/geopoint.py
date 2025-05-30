# model/geopoint.py
from dataclasses import dataclass

@dataclass
class GeoPoint:
    latitude: float
    longitude: float
