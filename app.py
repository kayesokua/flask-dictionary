from flask import Flask, redirect, render_template, request, url_for, jsonify, Response
import urllib.request
import json
import gtts
import random
from io import BytesIO

app = Flask(__name__)


# Requesting data from google sheets and reformatting
# Global Functions
dictionary_url = "https://sheets.googleapis.com/v4/spreadsheets/1b-ri2DlWLIhqB-E8xUCqnh9fsxJJ5J-KGV52rJ250Dk/values/main?alt=json&key=AIzaSyB1Wz6Hm3vj4KYuRdlZ8m4N5YB_GJnjF8k"
with urllib.request.urlopen(dictionary_url) as url:
    dictionary_data = json.load(url)
    dictionary_data = dictionary_data["values"]
    dictionary_data.pop(0)

    # To avoid case-sensitve searches
    dictionary_datac = list(map(lambda x: list(map(lambda y: y.casefold(), x)), dictionary_data))
dictionary_len = len(dictionary_datac)-1

# Route for home page that starts with a random word
@app.route("/")
def index():
    i = random.randint(0,dictionary_len)
    results = []
    random_item = {
        "type": dictionary_data[i][0],
        "en": dictionary_data[i][1],
        "de": dictionary_data[i][2],
        "zh-cn": dictionary_data[i][3],
        "pinyin": dictionary_data[i][4],
        "ph-tl": dictionary_data[i][5]
        }
    return render_template("home.html", random=random_item, masonry = False)

# Route for searching a keyword using Get Method
@app.route("/search", methods=["GET"])
def search_item():
    keyword = request.args.get('keyword')
    keyword = keyword.casefold()
    if keyword == '' or len(keyword) < 4:
        return redirect(url_for('index'))
    else:
        results = [sublist for sublist in dictionary_datac for item in sublist if keyword in item]
        return render_template("home.html",results=results,keyword=keyword, masonry=True)

# Generating speech URL for the audio source
@app.route("/speech/<lang>/<text>")
def generate_speech_url(lang,text):
    tts = gtts.gTTS(text=text, lang=lang)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return Response(fp.read(), content_type="audio/mpeg")

# API Routes
@app.route("/api/json/")
def get_api_json_all():
    return jsonify(dictionary_data)

@app.route("/api/json/<int:param>")
def get_api_json_one(param):
    i = int(param)
    try:
        result = {
            "type": dictionary_data[i][0],
            "en": dictionary_data[i][1],
            "de": dictionary_data[i][2],
            "zh-cn": dictionary_data[i][3],
            "pinyin": dictionary_data[i][4],
            "ph-tl": dictionary_data[i][5],
            }
        return jsonify(result)
    except IndexError:
        message = "At the moment, the dictionary only have {} items.".format(dictionary_len)
        return render_template("error.html",error=message)

@app.errorhandler(404)
@app.errorhandler(500)
def page_not_found(e):
    return render_template("error.html",error=e)

if __name__ == "__main__":
    app.run(debug = True)