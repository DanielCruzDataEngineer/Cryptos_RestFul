import requests
def get_crypto_options():
    url = 'https://min-api.cryptocompare.com/data/all/coinlist'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['Data']
        options = [{'label': data[k]['FullName'], 'value': data[k]['Symbol']} for k in data.keys()]
        return options
    else:
        print("Erro ao receber dados: código de status ", response.status_code)
        return []
