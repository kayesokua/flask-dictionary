from flask import Flask, redirect, render_template, request, url_for, jsonify
import urllib.request
import json
import gtts
from playsound import playsound
import time
import random

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
        "ph-tl": dictionary_data[i][5],
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

# Route for playing the phrase in the given language
@app.route("/<lang>/<input>")
def play(input,lang):
    tts = gtts.gTTS(input, lang=lang)
    tts.save("demo.mp3")
    playsound("demo.mp3")
    return redirect(request.referrer)

# Route for playing all audio with one click
@app.route("/play", methods=["GET"])
def play_quad():
    en = request.args.get('en')
    de = request.args.get('de')
    zh = request.args.get('zh')
    tl = request.args.get('tl')
    input_en = gtts.gTTS(en, lang='en')
    input_en.save("input_en.mp3")
    input_de = gtts.gTTS(de, lang='de')
    input_de.save("input_de.mp3")
    input_zh = gtts.gTTS(zh, lang='zh')
    input_zh.save("input_zh.mp3")
    input_tl = gtts.gTTS(tl, lang='tl')
    input_tl.save("input_tl.mp3")
    playsound("input_en.mp3")
    time.sleep(0.5)
    playsound("input_de.mp3")
    time.sleep(0.5)
    playsound("input_zh.mp3")
    time.sleep(0.5)
    playsound("input_tl.mp3")
    return redirect(request.referrer)

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