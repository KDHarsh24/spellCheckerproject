from spellchecker import SpellChecker

spell = SpellChecker()

def suggestpyspelling(word):
    """Return spelling suggestions for a word, or an empty list if the word exists."""
    
    # If the word exists in the PySpell dictionary, return an empty list
    if spell.known([word]):
        return []
    
    # Return list of suggested corrections
    return list(spell.candidates(word))