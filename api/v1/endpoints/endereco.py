from fastapi import APIRouter, Query

from typing import Dict

from core.dao import buscar_endereco
from core.schemas.address import AdressSearch



app = APIRouter()


@app.get('/geolocalizar_endereco/{endereco}', response_model=AdressSearch, tags=['geolocalizacao'])
async def geolocalizar_endereco(endereco:str, **camadas_geosampa:Dict[str, str]):

    data = buscar_endereco(endereco, **camadas_geosampa)

    return data