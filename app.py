import base64
import logging
import random
import sys
import traceback

from flask import Flask, make_response, jsonify, request
from flask_cors import CORS, cross_origin

from pixqrcodegen import Payload

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSON_SORT_KEYS'] = False


@app.route('/pix/gerar', methods=['POST'])
@cross_origin()
def gerar_qr_code():
    try:
        id_random = random.randint(0, 9)
        # Parâmetros necessários
        input = request.json
        payload = Payload(input['nome'], input['chave'], str(input['valor']), input['cidade'], str(id_random))
        payload.gerarPayload()

        with open("pixqrcodegen.png", "rb") as img:
            response = img.read()
        response = base64.b64encode(response)

        json_response = {
            "base64Img": response.decode('utf-8'),
            "codigoCompra": str(payload.payload_completa)
        }

        return make_response(jsonify(json_response), 200)
    except Exception as ex:
        traceback.print_exception(type(ex), ex, ex.__traceback__, file=sys.stderr)
        return make_response(jsonify({"error": "internal error {ex}".format(ex=ex)}))


if __name__ == '__main__':
    app.run(debug=True)
