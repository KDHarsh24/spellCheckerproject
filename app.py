from flask import Flask, request, jsonify, render_template
from trieDataStructure import Trie
from flask_cors import CORS
import string 
from symspell import symSpellCheck
from pyspell import suggestpyspelling

# Initialize Flask app
app = Flask(__name__, template_folder="templates")

# Allowed frontend domains
allowed_origins = [
    "https://triespellchecker.vercel.app",
    "https://triespellchecker-git-main-kdharsh24s-projects.vercel.app",
    "https://triespellchecker-pwhkt5s2m-kdharsh24s-projects.vercel.app"
]

CORS(app, resources={r"/*": {
    "origins": allowed_origins,
    "methods": ["GET", "POST"],
    "allow_headers": ["Content-Type", "Authorization"],
    "supports_credentials": True
}})

@app.route('/')
def home():
    return render_template("index.html")

# Initialize Trie and load dictionary
trieEn = Trie()
trieEn.load_from_file(filename='trie_data_eng.json')

@app.route('/spell-check', methods=['POST'])
def spell_check():
    data = request.json
    word = data.get("word", "").strip().lower().rstrip(string.punctuation)

    if not word:
        return jsonify({"error": "Word is required"}), 400

    if trieEn.search(word):
        return jsonify({"word": word, "suggestions": []})

    levenD = 2
    correct_words = []

    while not correct_words and levenD < len(word):
        correct_words = trieEn.find_similar_words(word, max_distance=levenD)
        levenD += 1

    return jsonify({"word": word, "suggestions": correct_words})


@app.route('/symspell', methods=['POST'])
def symspell():
    data = request.json
    word = data.get("word", "").strip().lower().rstrip(string.punctuation)

    if not word:
        return jsonify({"error": "Word is required"}), 400

    if trieEn.search(word):
        return jsonify({"word": word, "suggestions": []})

    correct_words = symSpellCheck(word)


    return jsonify({"word": word, "suggestions": correct_words})

@app.route('/pyspell', methods=['POST'])
def pyspell():
    data = request.json
    word = data.get("word", "").strip().lower().rstrip(string.punctuation)

    if not word:
        return jsonify({"error": "Word is required"}), 400

    if trieEn.search(word):
        return jsonify({"word": word, "suggestions": []})

    correct_words = suggestpyspelling(word)


    return jsonify({"word": word, "suggestions": correct_words})

if __name__ == '__main__':
    app.run(debug=True)
