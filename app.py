# .venv\Scripts\activate
# python -m flask run --debug

from flask import Flask, render_template, request, jsonify, send_file, make_response
import xml.etree.ElementTree as ET
from markupsafe import escape
from jinja2 import Environment, FileSystemLoader
from kanji_list import kanji
from kanjivg.kvg_lookup import commandFindSvg
from xmlhandler import listSvgFiles
import json

app = Flask(__name__)
selectedKanji = []

@app.route("/")
def index():
    return render_template('main.html')

@app.route("/select")
def select_kanji():
    return render_template('select.html', kanji = kanji)

@app.route("/overview")
def overview():
    sendIndex = request.args.get('selectedKanji')

    if sendIndex:
        sendIndex = json.loads(sendIndex)
    
    selectedKanji.clear()
    for index in sendIndex:
        selectedKanji.append(kanji[int(index)])

    print(selectedKanji)

    return render_template('overview.html', selectedKanji = selectedKanji)

@app.route("/writing")
def writing():
    return render_template('writing.html', selectedKanji = selectedKanji)

# @app.route("/test")
# def test():
#     send = request.args.get('selectedKanji')
#     if selectedKanji:
#         selectedKanji = json.loads(selectedKanji)
#     return render_template('test.html', selectedKanji = selectedKanji)

@app.route('/get-svg', methods=['POST'])
def get_svg():
    data = request.json
    kanji = data.get('kanji')
    kanji_path = commandFindSvg(kanji)
    return kanji_path

if __name__ == "__main__":
    app.run(debug=True)
