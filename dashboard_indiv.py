import requests
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from datetime import datetime, timedelta

# Define o endpoint da API CryptoCompare
url = 'https://min-api.cryptocompare.com/data/v2/histohour'
external_stylesheets = ['https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i']
# Define os parâmetros da solicitação
params = {
    'fsym': 'ETH',
    'tsym': 'USD',
    'limit': 24,
    'aggregate': 1,
    'api_key': 'd78f64e0e338fae8bd8b780db045c5756f40340f5df19329d16775cbc949306e'
}

# Função para obter os valores de preço e volume para o ETH
def get_data(symbol):
    params['fsym'] = symbol
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()['Data']['Data']
        df = pd.DataFrame(data)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df['pct_change'] = df['close'].pct_change()
        df['volatility'] = df['pct_change'].rolling(20).std() * np.sqrt(24)
        df.set_index('time', inplace=True)
        return df
    else:
        print("Erro ao receber dados: código de status ", response.status_code)
        return pd.DataFrame()


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

# Define o layout do dashboard
app = dash.Dash(__name__,external_stylesheets=external_stylesheets,serve_locally=False)
# Define as opções do dropdown
# options = [{'label': 'ETH', 'value': 'ETH'},
#            {'label': 'BTC', 'value': 'BTC'},
#            {'label': 'LTC', 'value': 'LTC'}]

options = get_crypto_options()
app.layout = html.Div(children=[
    html.H1(children='Crypto Dashboard', style={'textAlign': 'center','color':'white'}),
    dcc.Dropdown(id='crypto-dropdown', options=options, value='ETH',style={'color':'blue','backgroundColor':'black'}),
    dcc.Graph(id='price-chart'),
    dcc.Graph(id='volume-chart'),
    dcc.Graph(id='volatility-chart'),
    dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0)
],style={'backgroundColor':'black', 'color': 'white', 'font-family': 'sans-serif', 'margin': '0px', 'padding': '0px'})
# Define o estilo CSS global
app.css.append_css({
    'external_url': 'https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css'
})

# Define o estilo CSS para o corpo da página
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

# Define o estilo CSS para os gráficos
app.css.append_css({
    'external_url': 'https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i'
})
# Define as funções de atualização dos gráficos
@app.callback(Output('price-chart', 'figure'),
              Output('volume-chart', 'figure'),
              Output('volatility-chart', 'figure'),
              Input('crypto-dropdown', 'value'),
              Input('interval-component', 'n_intervals'))
def update_charts(symbol, n):
    # Obtém os dados atualizados
    df = get_data(symbol)

    # Cria o layout dos gráficos atualizados
    price_fig = {
        'data': [go.Scatter(x=df.index, y=df['close'], mode='lines', name='Preço')],
        'layout': go.Layout(title=f'Preço do {symbol} (USD)', xaxis=dict(title='Tempo'), yaxis=dict(title='Preço (USD)'), template='plotly_dark',plot_bgcolor="rgba(0,0,0,0)",  # define o fundo do gráfico como transparente
    paper_bgcolor="rgba(0,0,0,0)")
    }
    
    volume_fig = {
        'data': [go.Bar(x=df.index, y=df['volumeto'], name='Volume')],
        'layout': go.Layout(title=f'Volume do {symbol} (USD)', xaxis=dict(title='Tempo'), yaxis=dict(title='Volume (USD)'), template='plotly_dark',plot_bgcolor="rgba(0,0,0,0)",  # define o fundo do gráfico como transparente
    paper_bgcolor="rgba(0,0,0,0)")
}
    volatility_fig = {
        'data': [go.Candlestick(x=df.index, open=df['open'], high=df['high'], low=df['low'], close=df['close'], name='Candlestick')],
        'layout': go.Layout(title=f'Candlestick do {symbol}', xaxis_title='Hora (24 horas atrás - Agora)', yaxis_title='Candlestick', template='plotly_dark',plot_bgcolor="rgba(0,0,0,0)",  # define o fundo do gráfico como transparente
        paper_bgcolor="rgba(0,0,0,0)")
}    # Retorna os gráficos atualizados
    return price_fig, volume_fig, volatility_fig

if __name__=='__main__':
    app.run_server(debug=True)