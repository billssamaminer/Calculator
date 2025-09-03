from flask import Flask, jsonify
from flask_cors import CORS
import requests, json, os

app = Flask(__name__)
CORS(app)  # Permite llamadas desde cualquier origen

def obtener_precio_usdt_ves():
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {
        "proMerchantAds": False,
        "page": 1,
        "rows": 100,
        "payTypes": ["Mercantil"],
        "countries": [],
        "publisherType": None,
        "asset": "USDT",
        "fiat": "VES",
        "tradeType": "SELL"
    }
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Host": "p2p.binance.com",
        "Origin": "https://p2p.binance.com"
    }
    try:
        resp = requests.post(url, headers=headers, data=json.dumps(payload))
        datos = resp.json()
        if datos['data'] and len(datos['data']) > 0:
            anuncio = datos['data'][40]
            return {
                "comerciante": anuncio['advertiser']['nickName'],
                "precio": anuncio['adv']['price'],
                "disponible": anuncio['adv']['surplusAmount']
            }
        else:
            return {"error": "No se encontraron anuncios"}
    except Exception as e:
        return {"error": str(e)}

@app.route('/usdt', methods=['GET'])
def usdt():
    return jsonify(obtener_precio_usdt_ves())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render usa la variable PORT
    app.run(host="0.0.0.0", port=port)




