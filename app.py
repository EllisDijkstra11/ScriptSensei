# .venv\Scripts\activate
# python -m flask run --debug

from flask import Flask, render_template, request, jsonify, send_file, make_response
import xml.etree.ElementTree as ET
from markupsafe import escape
from jinja2 import Environment, FileSystemLoader
from svgpathtools import parse_path
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
    svg_paths = extractSVGPaths(kanji_path)
    print('SVG paths:', svg_paths)

    svg_points = []
    for path in svg_paths:
        svg_points.append(svgPathToPoints(path))

    return svg_points  

def extractSVGPaths(svg_path):
    try:
        tree = ET.parse(svg_path)  # Parse SVG file directly from path
        root = tree.getroot()
        paths = []
        for elem in root.iter():
            if elem.tag.endswith('path'):
                paths.append(elem.attrib['d'])
        return paths
    except Exception as e:
        print(f"Error parsing SVG file {svg_path}: {e}")
        return []
    
def svgPathToPoints(path_data):
    path = parse_path(path_data)
    points = []
    
    for segment in path:
        if segment.start is not None:
            points.append([segment.start.real, segment.start.imag])
        
        if segment.end is not None:
            points.append([segment.end.real, segment.end.imag])
    
    return points

if __name__ == "__main__":
    app.run(debug=True)
