from trieDataStructure import Trie
import string
trie = Trie()
trie.load_from_file()

def triespellChecker(word):
    word = word.strip().lower().rstrip(string.punctuation)
    correct_words = []
    levenD = 2
    while not correct_words and levenD < len(word):
        correct_words = trie.find_similar_words(word, max_distance=levenD)
        levenD += 1
    return correct_words
# print(triespellChecker('speling'))