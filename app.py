from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import string 
from algorithms.triespell import triespellChecker
from algorithms.symspell import symSpellCheck
from algorithms.pyspell import suggestpyspelling

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


@app.route('/<language>/spell-check', methods=['POST'])
def spell_check(language):
    data = request.json
    word = data.get("word", "").strip().lower().rstrip(string.punctuation)
    if not word:
        return jsonify({"error": "Word is required"}), 400
    correct_words = triespellChecker(word, language)
    return jsonify({"word": word, "suggestions": correct_words})


@app.route('/<language>/symspell', methods=['POST'])
def symspell(language):
    data = request.json
    word = data.get("word", "").strip().lower().rstrip(string.punctuation)

    if not word:
        return jsonify({"error": "Word is required"}), 400

    correct_words = symSpellCheck(word)
    return jsonify({"word": word, "suggestions": correct_words})

@app.route('/<language>/pyspell', methods=['POST'])
def pyspell():
    data = request.json
    word = data.get("word", "").strip().lower().rstrip(string.punctuation)

    if not word:
        return jsonify({"error": "Word is required"}), 400
    correct_words = suggestpyspelling(word)
    return jsonify({"word": word, "suggestions": correct_words})

if __name__ == '__main__':
    app.run(debug=True)
