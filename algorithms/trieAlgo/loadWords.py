from trieDataStructure import Trie
import json

trie = Trie()

trie.load_from_file(filename='./algorithms/treeData/trie_data_ben.json')
def load_words():
    with open('./algorithms/treeData/bengaliwords.txt', encoding='utf-8') as word_file:
        words = word_file.read().lower().split()
        valid_words = [word for word in words if len(word) > 1]
    return valid_words

word_list = load_words()
for word in word_list:
    trie.insert(word)
trie.save_to_file(filename='./algorithms/treeData/trie_data_ben.json')



# def load_words(json_filename):
#     """Load a set of correct words from a JSON file."""
#     with open(json_filename, "r", encoding="utf-8") as word_file:
#         word_data = json.load(word_file)  # Load JSON data

#     # Ensure words are in a list or set format
#     if isinstance(word_data, dict):
#         valid_words = set(word_data.values())  # If JSON is a dictionary, get values
#     elif isinstance(word_data, list):
#         valid_words = set(word_data)  # If JSON is a list, convert it to a set
#     else:
#         raise ValueError("Invalid JSON format. Expected a dictionary or list.")

#     return valid_words

# # Usage Example
# json_filename = "spell_check_data.json"  # Change this to your actual JSON file
# word_list = list(load_words(json_filename))
# for word in word_list:
#     trie.insert(word)
# trie.save_to_file()
# # Test Output
# print(f"✅ Loaded {len(word_list)} words from JSON.")
