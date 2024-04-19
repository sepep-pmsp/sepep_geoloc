from pydantic import BaseModel, model_validator
from typing import List, Dict, Optional
from core.utils.geo import within_sao_paulo_bbox
from .geojson import GeoJson
from .camadas import CamadaParam

class Point(BaseModel):

    x: float
    y: float

    @model_validator(mode='after')
    def in_sp_bbox(self):

        if not within_sao_paulo_bbox(self.x, self.y):
            raise ValueError('Must be within Sao Paulo bbox.')

        return self

class PointSearch(BaseModel):

    point: Point
    camadas: List[CamadaParam]

class PointResponse(BaseModel):

    point: GeoJson
    camadas_geosampa: Dict[str, GeoJson]