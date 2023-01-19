from flask import Flask
import urllib.request
import json

app = Flask(__name__)

dictionary_url = "https://sheets.googleapis.com/v4/spreadsheets/1b-ri2DlWLIhqB-E8xUCqnh9fsxJJ5J-KGV52rJ250Dk/values/main?alt=json&key=AIzaSyB1Wz6Hm3vj4KYuRdlZ8m4N5YB_GJnjF8k"
with urllib.request.urlopen(dictionary_url) as url:
    dictionary_data = json.load(url)
    dictionary_data = dictionary_data["values"]
    dictionary_data.pop(0)

@app.route("/")
def get_dictionary():
    return json.dumps(dictionary_data, ensure_ascii=False)


@app.route("/<int:param>")
def get_dictionary_item(param):
    i = int(param)
    result = {
        "type": dictionary_data[i][0],
        "en": dictionary_data[i][1],
        "de": dictionary_data[i][2],
        "zh-cn": dictionary_data[i][4],
        "zh-tw": dictionary_data[i][5],
        "pinyin": dictionary_data[i][6],
        "ph-tl": dictionary_data[i][7],
        "es": dictionary_data[i][8]
        }
    return json.dumps(result, ensure_ascii=False)

@app.errorhandler(404)
@app.errorhandler(500)
def page_not_found(e):
    return "Dictionary is still on beta mode. Only acceptable endpoints are digits 0 - 478"

if __name__ == "__main__":
    app.run(debug = True)