from pydantic import BaseModel
from typing import List, Dict, Optional
from .geojson import GeoJson, Feature

class AdressSearch(BaseModel):

    endereco: GeoJson
    camadas_geosampa: Dict[str, GeoJson]