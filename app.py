from flask import Flask, redirect, render_template, request, url_for, jsonify, Response
import urllib.request
import json
import gtts
import random
from io import BytesIO

app = Flask(__name__)

class DictionaryAPI:
    def __init__(self):
        self.dictionary_url = "https://sheets.googleapis.com/v4/spreadsheets/1b-ri2DlWLIhqB-E8xUCqnh9fsxJJ5J-KGV52rJ250Dk/values/main?alt=json&key=AIzaSyB1Wz6Hm3vj4KYuRdlZ8m4N5YB_GJnjF8k"
        with urllib.request.urlopen(self.dictionary_url) as url:
            self.dictionary_data = json.load(url)
            self.dictionary_data = self.dictionary_data["values"]
            self.dictionary_data.pop(0)
            self.dictionary_datac = list(map(lambda x: list(map(lambda y: y.casefold(), x)), self.dictionary_data))
        self.dictionary_len = len(self.dictionary_datac) - 1

    def search(self, keyword):
        keyword = keyword.casefold()
        if keyword == '' or len(keyword) < 4:
            return None
        else:
            results = [sublist for sublist in self.dictionary_datac for item in sublist if keyword in item]
            return results

    def get_random(self):
        i = random.randint(0, self.dictionary_len - 1)
        random_item = {
            "type": self.dictionary_data[i][0],
            "en": self.dictionary_data[i][1],
            "de": self.dictionary_data[i][2],
            "zh-cn": self.dictionary_data[i][3],
            "pinyin": self.dictionary_data[i][4],
            "ph-tl": self.dictionary_data[i][5]
        }
        return random_item

    def get_json_all(self):
        return jsonify(self.dictionary_data)

    def get_json_one(self, param):
        i = int(param)
        try:
            result = {
                "type": self.dictionary_data[i][0],
                "en": self.dictionary_data[i][1],
                "de": self.dictionary_data[i][2],
                "zh-cn": self.dictionary_data[i][3],
                "pinyin": self.dictionary_data[i][4],
                "ph-tl": self.dictionary_data[i][5],
            }
            return jsonify(result)
        except IndexError:
            message = "At the moment, the dictionary only have {} items.".format(self.dictionary_len)
            return render_template("error.html", error=message)

dictionary_api = DictionaryAPI()

# Home page and search functionality:
@app.route("/")
def index():
    random_item = dictionary_api.get_random()
    return render_template("home.html", random=random_item, masonry = False)

@app.route("/search")
def search_item():
    keyword = request.args.get('keyword')
    results = dictionary_api.search(keyword)
    return render_template("home.html",results=results,keyword=keyword, masonry=True)

# Speech generation
@app.route("/speech/<lang>/<text>")
def generate_speech_url(lang,text):
    tts = gtts.gTTS(text=text, lang=lang)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return Response(fp.read(), content_type="audio/mpeg")

#API endpoints
@app.route("/api/json/")
def get_api_json_all():
    return dictionary_api.get_json_all()

@app.route("/api/json/<int:param>")
def get_api_json_one(param):
    return dictionary_api.get_json_one(int(param))

#Error handling:
@app.errorhandler(404)
@app.errorhandler(500)
def page_not_found(e):
    return render_template("error.html",error=e)

if __name__ == "__main__":
    app.run(debug = True)