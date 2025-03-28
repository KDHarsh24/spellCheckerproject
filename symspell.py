import pkg_resources
from symspellpy import SymSpell, Verbosity

# Initialize SymSpell
sym_spell = SymSpell(max_dictionary_edit_distance=2)

# Load a prebuilt English dictionary
dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

def symSpellCheck(word):
    """Return spelling suggestions for a single word."""
    suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2, include_unknown=True)
    return [suggestion.term for suggestion in suggestions[:5]]

# Example Usage
# word = "spleling"
# suggestions = symSpellCheck(word)

# print("Original:", word)
# print("Suggestions:", suggestions)
