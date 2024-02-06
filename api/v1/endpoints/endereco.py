from fastapi import APIRouter, Query

from typing import List

from core.dao import buscar_endereco
from core.schemas.address import AdressSearch, AdressSearchParameters



app = APIRouter()


@app.post('/geolocalizar_endereco/', response_model=List[AdressSearch], tags=['geolocalizacao'])
async def geolocalizar_endereco(search_endereco:AdressSearchParameters):

    endereco = search_endereco.endereco
    camadas = search_endereco.camadas

    if camadas:
        camadas_geosampa = {camada.alias:camada.layer_name for camada in camadas}
    else:
        camadas_geosampa={}
    data = buscar_endereco(endereco, **camadas_geosampa)

    return data