import os
from symspellpy import SymSpell, Verbosity

# Initialize SymSpell
max_edit_distance = 2
prefix_length = 7
sym_spell = SymSpell(max_dictionary_edit_distance=max_edit_distance, prefix_length=prefix_length)

# Load custom dictionary (20k.txt)
dictionary_path = './algorithms/treeData/20k.txt'
if os.path.exists(dictionary_path):
    if not sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1):
        print("❌ Error: Failed to load dictionary contents.")
        exit()
else:
    print(f"❌ Error: Dictionary file not found at {dictionary_path}")
    exit()

print("✅ Dictionary loaded successfully!")

def symSpellCheck(word):
    """
    Return spelling suggestions for a single word.
    If word is correct (exists in dictionary), returns empty list.
    """
    word = word.lower()
    
    if word in sym_spell.words:
        return []

    suggestions = sym_spell.lookup(
        word,
        Verbosity.CLOSEST,
        max_edit_distance=max_edit_distance,
        include_unknown=True
    )

    return [suggestion.term for suggestion in suggestions[:5]]

# Example usage
if __name__ == "__main__":
    word = "wrng"
    suggestions = symSpellCheck(word)

    print("Original:", word)
    print("Suggestions:", suggestions)
