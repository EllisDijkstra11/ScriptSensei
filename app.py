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

@app.route('/check_kanji', methods=['POST'])
def check_kanji():
    data = request.json
    kanji = data.get('kanji')
    input_array = data.get('array')

    try:
        kanji_path = commandFindSvg(kanji)
    except FileNotFoundError:
        return jsonify({'error': 'Kanji SVG file not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Error finding SVG path: {str(e)}'}), 500

    svg_paths = extractSVGPaths(kanji_path)

    template_array = []
    for path in svg_paths:
        template_array.append(svgPathToPoints(path))

    print("input_data =", input_array)
    print("template_data =", template_array)
    feedback = compare_kanji(input_array, template_array)
    return jsonify({'score': feedback})

if __name__ == "__main__":
    app.run(debug=True)
