import requests
from api.config import load_env

# Configurações
subscription_key = load_env('AZURE_KEY')  # Substitua pela sua chave do Azure Maps
address = 'Viaduto do Chá, nº 15'  # Endereço para geocodificação
url = f'https://atlas.microsoft.com/search/address/json'

# Parâmetros para a requisição
params = {
    'subscription-key': subscription_key,
    'api-version': '1.0',
    'query': address,
}

# Fazendo a requisição
response = requests.get(url, params=params)

# Verificando e exibindo os resultados
if response.status_code == 200:
    data = response.json()
    results = data.get('results')
    if results:
        print(results)
        latitude = results[0]['position']['lat']
        longitude = results[0]['position']['lon']
        print(f"Coordenadas para '{address}':")
        print(f"Latitude: {latitude}, Longitude: {longitude}")
    else:
        print("Nenhum resultado encontrado para o endereço.")
else:
    print(f"Erro {response.status_code}: {response.text}")


from api.core.integrations.azure import azure_maps_address_search

results = azure_maps_address_search('Viaduto do Chá, nº 15')
print(results)