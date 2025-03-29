from algorithms.trieAlgo.trieDataStructure import Trie
import string
trieEn = Trie()
trieEn.load_from_file(filename='../treeData/trie_data_eng.json')
trieBn = Trie()
trieBn.load_from_file(filename='../treeData/trie_data_ben.json')
trieHi = Trie()
trieHi.load_from_file(filename='../treeData/trie_data_hi.json')

def triespellChecker(word, lang):
    word = word.strip().lower().rstrip(string.punctuation)
    correct_words = []
    levenD = 2
    if lang == 'english':
        while not correct_words and levenD < len(word):
            correct_words = trieEn.find_similar_words(word, max_distance=levenD)
            levenD += 1
    elif lang == 'bengali':
        while not correct_words and levenD < len(word):
            correct_words = trieBn.find_similar_words(word, max_distance=levenD)
            levenD += 1
    elif lang == 'hindi':
        while not correct_words and levenD < len(word):
            correct_words = trieHi.find_similar_words(word, max_distance=levenD)
            levenD += 1
    return correct_words

