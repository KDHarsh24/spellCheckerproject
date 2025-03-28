import json

class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """Insert a word into the Trie"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.end = True

    def search(self, word):
        """Check if a word exists in the Trie"""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.end

    def find_similar_words(self, word, max_distance=2):
        """Find closest words using Trie traversal & Damerau-Levenshtein distance"""
        results = []
        self._traverse_trie(self.root, "", word.lower(), max_distance, results)
        results.sort(key=lambda x: (x[1], -self.common_chars(word, x[0]))) 
        candidates = [w[0] for w in results]
        # print(candidates)
        if candidates:
            return self.refine_with_ord(word, candidates)
        return candidates

    def _traverse_trie(self, node, current_word, target_word, max_distance, results):
        """Recursively traverse the Trie and compute Damerau-Levenshtein distance"""
        if node.end:
            distance = self.damerau_levenshtein_distance(current_word, target_word)
            if distance <= max_distance:
                results.append((current_word, distance))

        for char, child_node in node.children.items():
            self._traverse_trie(child_node, current_word + char, target_word, max_distance, results)

    def refine_with_ord(self, word, candidates):
        """Refine suggestions based on character similarity, position matching, and total character overlap.
        Returns the top 4 best matches sorted by these criteria.
        """

        def position_similarity(w1, w2):
            """Calculate position-based similarity score: +1 for each character that matches at the same index."""
            return sum(1 for i in range(min(len(w1), len(w2))) if w1[i] == w2[i])

        def total_char_match(w1, w2):
            """Count how many characters match in total, ignoring order."""
            return sum(min(w1.count(char), w2.count(char)) for char in set(w1))

        sorted_candidates = sorted(
            candidates,
            key=lambda w: (
                -self.common_chars(word, w),   # More common characters first
                -position_similarity(word, w), # More character matches at the same index
                -total_char_match(word, w),    # More total character overlap
                abs(len(w) - len(word))        # Smaller length difference first
            )
        )
        print("all the possible Words", sorted_candidates)
        return sorted_candidates[:5] if len(sorted_candidates) > 5 else sorted_candidates


    
    def common_chars(self, word1, word2):
        """Count the number of common characters in two words"""
        return sum(1 for c in word1 if c in word2)

    @staticmethod
    def damerau_levenshtein_distance(s1, s2):
        """Compute Damerau-Levenshtein Distance"""
        len_s1, len_s2 = len(s1), len(s2)
        dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

        for i in range(len_s1 + 1):
            for j in range(len_s2 + 1):
                if i == 0:
                    dp[i][j] = j
                elif j == 0:
                    dp[i][j] = i
                elif s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

                if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                    dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + 1)

        return dp[len_s1][len_s2]

    
    def to_dict(self, node=None):
        """Convert Trie to dictionary for JSON storage"""
        if node is None:
            node = self.root
        return {
            'children': {char: self.to_dict(child) for char, child in node.children.items()},
            'end': node.end
        }

    def save_to_file(self, filename="trie_data.json"):
        """Save Trie to JSON file"""
        with open(filename, "w") as file:
            json.dump(self.to_dict(), file, indent=4)

    def from_dict(self, data, node=None):
        """Load Trie from dictionary"""
        if node is None:
            node = self.root
        node.end = data.get('end', False)
        for char, child_data in data.get('children', {}).items():
            node.children[char] = TrieNode()
            self.from_dict(child_data, node.children[char])

    def load_from_file(self, filename="trie_data.json"):
        """Load Trie from JSON file"""
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                self.from_dict(data)
        except FileNotFoundError:
            print(f"⚠️ File '{filename}' not found. Starting with an empty Trie.")


# trie = Trie()

# trie.load_from_file()
# def load_words():
#     with open('wiki-100k.txt', encoding='utf-8') as word_file:
#         valid_words = set(word_file.read().lower().split())
#     return valid_words
# word_list = load_words()
# for word in word_list:
#     trie.insert(word)
# trie.save_to_file()

