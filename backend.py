from flask import Flask, request, jsonify
from trieDataStructure import Trie
from flask_cors import CORS
import string 
from symspell import symSpellCheck
from pyspell import suggestpyspelling

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS if needed

# Initialize Trie and load dictionary
trie = Trie()
trie.load_from_file()

@app.route('/spell-check', methods=['POST'])
def spell_check():
    data = request.json
    word = data.get("word", "").strip().lower().rstrip(string.punctuation)

    if not word:
        return jsonify({"error": "Word is required"}), 400

    if trie.search(word):
        return jsonify({"word": word, "suggestions": []})

    levenD = 2
    correct_words = []

    while not correct_words and levenD < len(word)-1:
        correct_words = trie.find_similar_words(word, max_distance=levenD)
        levenD += 1

    return jsonify({"word": word, "suggestions": correct_words})


@app.route('/symspell', methods=['POST'])
def symspell():
    data = request.json
    word = data.get("word", "").strip().lower().rstrip(string.punctuation)

    if not word:
        return jsonify({"error": "Word is required"}), 400

    if trie.search(word):
        return jsonify({"word": word, "suggestions": []})

    correct_words = symSpellCheck(word)


    return jsonify({"word": word, "suggestions": correct_words})

@app.route('/pyspell', methods=['POST'])
def pyspell():
    data = request.json
    word = data.get("word", "").strip().lower().rstrip(string.punctuation)

    if not word:
        return jsonify({"error": "Word is required"}), 400

    if trie.search(word):
        return jsonify({"word": word, "suggestions": []})

    correct_words = suggestpyspelling(word)


    return jsonify({"word": word, "suggestions": correct_words})

if __name__ == '__main__':
    app.run(debug=True)
