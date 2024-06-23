# .venv\Scripts\activate
# python -m flask run --debug

from flask import Flask, render_template, request, jsonify, send_file, make_response
from markupsafe import escape
from jinja2 import Environment, FileSystemLoader
from kanji_list import kanji
from kanjivg.kvg_lookup import find_svg
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
    kanji_character = data.get('kanji')
    svg_content = find_svg(kanji_character)
    
    if svg_content is None:
        return jsonify({"error": "Kanji not found"}), 404
    
    return jsonify({"svg": svg_content})

# Function to get the SVG path for the kanji character
def get_svg_for_kanji(kanji):
    svg_directory = "./kanji"  # Directory where your SVG files are located
    svg_filename = f"{kanji}.svg"  # Assuming SVG files are named by the kanji character
    svg_path = os.path.join(svg_directory, svg_filename)
    if os.path.isfile(svg_path):
        return svg_path
    else:
        return None

@app.route('/get_svg_part')
def get_svg_part():
    kanji = request.args.get('kanji')
    element_id = request.args.get('id')
    svg_path = get_svg_for_kanji(kanji)
    
    if not svg_path or not element_id:
        return jsonify({"error": "SVG or element ID not found"}), 404
    
    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()
        
        # Namespace handling (if any)
        ns = {'svg': 'http://www.w3.org/2000/svg'}
        
        element = root.find(f".//*[@id='{element_id}']", ns)
        
        if element is None:
            return jsonify({"error": "Element not found"}), 404
        
        element_string = ET.tostring(element, encoding='unicode')
        return make_response(element_string)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
