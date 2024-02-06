from pydantic import BaseModel, validator
from typing import Dict

from .geojson import GeoJson


class AdressSearch(BaseModel):

    endereco: GeoJson
    camadas_geosampa: Dict[str, GeoJson]

    