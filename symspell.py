import os
from symspellpy import SymSpell, Verbosity

# Get the absolute path of the dictionary file
dictionary_path = os.path.join(os.path.dirname(__file__), "frequency_dictionary_en_82_765.txt")

# Initialize SymSpell
sym_spell = SymSpell(max_dictionary_edit_distance=2)

# Load dictionary if available
if os.path.exists(dictionary_path):
    sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
else:
    print(f"Error: Dictionary file not found at {dictionary_path}")

def symSpellCheck(word):
    """Return spelling suggestions for a single word."""
    suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2, include_unknown=True)
    return [suggestion.term for suggestion in suggestions[:5]]

# Example usage
# word = "spleling"
# suggestions = symSpellCheck(word)

# print("Original:", word)
# print("Suggestions:", suggestions)
