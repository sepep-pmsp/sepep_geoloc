from fastapi import APIRouter, Query

from typing import List

from core.dao import listar_camadas, detalhar_camada
from core.schemas.camadas import CamadaBasico, DetalhesCamada



app = APIRouter()


@app.get('/camadas_geosampa', response_model=List[CamadaBasico], tags=['geosampa'])
async def list_camadas():
    '''Lista as camadas disponíveis para integração com o GeoSampa.'''

    camadas = listar_camadas()

    return camadas

@app.get('/camadas_geosampa/{layer_name}', response_model=DetalhesCamada)
async def detalhes_camada(layer_name:str):
    '''Apresenta o schema (propriedades e tipos de dado) da camada selecionada,
    além de identificar o tipo de geometria e qual o nome do atributo que contém a geometria.'''

    return detalhar_camada(layer_name)

