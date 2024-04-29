import pandas as pd

from flask import Flask, request, make_response, jsonify
from parser import Parser


application = Flask(__name__)

parser = Parser()
act_types = [
    {"label": "Яндекс", 'value': "YNDX"},
    {"label": "Сбер", 'value': "SBER"},
    {"label": "Гаспром", 'value': "GAZP"},
    {"label": "Лукойл", 'value': "LKOH"},
    {"label": "Магнит", 'value': "MGNT"},
    {"label": "Роснефть", 'value': "ROSN"},
    {"label": "ВТБ", 'value': "VTBR"},
    {"label": "НОВАТЕК", 'value': "NVTK"},
    {"label": "Сургутнефтегаз", 'value': "SNGS"}
]
models = {}

for i in act_types:
    with open("./models/model_" + i['value'] + ".bf", "rb") as file:
        models[i["value"]] = pd.read_pickle(file)


@application.route('/model/api/v1/get_preds/', methods=['POST'])
def get_preds():
    json = request.json
    result = models[json["value"]].get_forecast(steps=json["steps"]).predicted_mean
    return make_response(jsonify({"result": result.to_list()}), 201)


if __name__ == "__main__":
    # print(datetime.datetime.now().date().strftime("%d.%m.%Y"))
    application.run(host="0.0.0.0", port=9462)
    # bytes_ = bytes(pd.DataFrame(data=[[1, 2], [2, 3]]).to_csv(index=False), encoding="utf-8")
    # print(pd.read_csv(io.StringIO(bytes_)))
