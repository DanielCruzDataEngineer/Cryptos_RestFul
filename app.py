from flask import Flask, jsonify
from crypto_selector import get_crypto_options
from dashboard_indiv import get_data
import json
import datetime
app = Flask(__name__)

@app.route("/")
def get_options():
    options = get_crypto_options()
    return jsonify(options)


@app.route("/<crypto>")
def get_crypto_data(crypto):
    data = get_data(crypto)

    # adiciona a coluna de tempo
    data = data.reset_index()
    data = data.rename(columns={'index': 'time'})
    data_json = data.to_json(orient='index')
    data_dict = json.loads(data_json)

    # formata a coluna de tempo
    for key in data_dict:
        timestamp = data_dict[key]['time'] / 1000
        formatted_time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        data_dict[key]['time'] = formatted_time

    return jsonify(data_dict)


if __name__ == '__main__':
    app.run(debug=True)
