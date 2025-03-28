from spellchecker import SpellChecker

spell = SpellChecker()

def suggestpyspelling(word):
    return list(spell.candidates(word))  # Returns multiple suggestions
 # Example usage