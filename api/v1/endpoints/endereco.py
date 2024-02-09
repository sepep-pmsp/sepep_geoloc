from fastapi import APIRouter, Query

from typing import List

from core.dao import buscar_endereco, buscar_endereco_simples
from core.schemas.address import AdressSearch, AdressSearchParameters, GeoJsonEndereco



app = APIRouter()


@app.post('/geolocalizar_endereco', tags=['geolocalizacao'])
async def geolocalizar_endereco(search_endereco:AdressSearchParameters)->List[AdressSearch]:
    '''Realiza a busca do endereço (geolocalização). Permite a integração com o GeoSampa por meio do parâmetro 'camadas_geosampa'.
    Para cada uma das camadas selecionadas, a ferramenta irá identificar o(s) objeto(s) da camada que intersectam o ponto que representa o 
    endereço, conforme retornado pela geolocalização'''

    endereco = search_endereco.endereco
    camadas = search_endereco.camadas

    if camadas:
        camadas_geosampa = {camada.alias:camada.layer_name for camada in camadas}
    else:
        camadas_geosampa={}
    data = buscar_endereco(endereco, **camadas_geosampa)

    return data

@app.get('/geolocalizar_endereco_simples/{endereco}', tags=['geolocalizacao'])
async def geolocalizar_endereco_simples(endereco:str)->GeoJsonEndereco:
    '''Realiza a geolicalização do endereço apenas, sem integração com o GeoSampa.'''

    endereco = buscar_endereco_simples(endereco)

    return endereco