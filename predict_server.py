import json
from flask import Flask, send_from_directory, request, jsonify

import draw_text
from api_helpers import get_lyrics
from config import categories
from data_helpers import tokenize_and_process, pos_tagger
from draw_text import create_text_diagram
from model_persistance_helper import get_models_info, find_model

app = Flask(__name__)
app.debug = True

@app.route('/')
def main():
    return app.send_static_file('index.html')

@app.route('/models')
def models():
    return jsonify(get_models_info())


@app.route('/analyze')
def analyze():
    res = {
        "text": "Error",
        "code": 1
    }

    artist = request.args.get('artist')
    song = request.args.get('song')
    model_name = request.args.get('model_name')
    model_date = request.args.get('model_date')

    if not artist or not song or not model_name or not model_date:
        res["text"] = "Not enough parameters, got: {}".format(json.dumps(request.args))
        return jsonify(res)

    lyrics = get_lyrics(artist, song)

    if lyrics:
            model = find_model(model_name, model_date)
            if model:
                probabilities = model.predict_proba([tokenize_and_process(lyrics, pos_tagger)])[0]
                probabilities_with_labels = []
                for i, proba in enumerate(probabilities):
                    probabilities_with_labels.append(
                        {
                            "label": categories[i],
                            "probability": proba
                        }
                    )
                res["probabilities"] = probabilities_with_labels
                res["code"] = 0
                res["text"] = "OK"

                res["diagram_url"] = "image/" + create_text_diagram(model, lyrics, song)
            else:
                res["text"] = "Model not found: {}".format(json.dumps(request.args))
    else:
        res["text"] = "Song not found"

    return jsonify(res)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/image/<path:path>')
def send_image(path):
    return send_from_directory('image', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    app.run(host='0.0.0.0')
