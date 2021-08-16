import traceback
from main_app import main
from flask import Flask, request

app = Flask(__name__)

tasks_limit, tasks = 5, 0

default_params = {
    "lang": "en",
    "plac": "eg",
    "num": 10,
    "keyword": "what is discourse",
    "ques_num": 15,
    "resp_type": "HTML",
}


@app.route("/api", methods=['POST'])
def api_():
    global tasks
    json_data = get_json(request)

    if "4P1K3Y" in json_data.keys() and json_data["4P1K3Y"] == "7H1515MY4P1K3Y":
        json_data, err = full_featured(json_data, default_params)
        if err:
            return {"ERROR": err}
        elif tasks >= tasks_limit:
            return "server is busy"
        else:
            tasks += 1
            ques = main(json_data)
            tasks -= 1
            return ques
    return "key not valid" + str(json_data.items())


def get_json(request):
    json_data = dict()
    try:
        json_data = request.get_json(force=True)
    except:
        pass  # traceback.print_exc()
    if not json_data:
        try:
            json_data = request.form.to_dict()  # dict()
        except:
            traceback.print_exc()
    return json_data


def full_featured(dict1, default):
    err = ""
    for i, j in default.items():
        if i not in dict1.keys():
            dict1.update({i: j})
    for i, j in dict1.items():
        if i not in default.keys() and not i == "4P1K3Y":
            err += "KEY " + i + " IS NOT VALID"
    return dict1, err


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
