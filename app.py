# .venv\Scripts\activate
# python -m flask run --debug

from flask import Flask, render_template, request, jsonify, send_file, make_response
from markupsafe import escape
from jinja2 import Environment, FileSystemLoader
import json

from kanji_list import kanji
from kanjivg.kvg_lookup import commandFindSvg
from xmlhandler import listSvgFiles
from retrieve_SVG import extractSVGPaths, svgPathToPoints
from compare_kanji import compare_kanji

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

@app.route('/check_kanji', methods=['POST'])
def check_kanji():
    print("I'm here")
    data = request.json
    kanji = data.get('kanji')
    input_array = data.get('array')
    kanji_path = commandFindSvg(kanji)
    svg_paths = extractSVGPaths(kanji_path)

    template_array = []
    for path in svg_paths:
        template_array.append(svgPathToPoints(path))

    compare_kanji(input_array, template_array)
    return template_array



if __name__ == "__main__":
    app.run(debug=True)
