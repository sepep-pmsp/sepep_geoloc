from fastapi import APIRouter, Query

from typing import List

from core.dao import listar_camadas, detalhar_camada
from core.schemas.camadas import CamadaBasico, DetalhesCamada



app = APIRouter()


@app.get('/camadas_geosampa', response_model=List[CamadaBasico], tags=['geosampa'])
async def list_camadas():

    camadas = listar_camadas()

    return camadas

@app.get('/camadas_geosampa/{layer_name}', response_model=DetalhesCamada)
async def detalhar_camada(layer_name:str):

    return detalhar_camada(layer_name)

