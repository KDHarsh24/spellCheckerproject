import json
import time
from tqdm import tqdm
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from Levenshtein import distance as levenshtein_distance
from algorithms.triespell import triespellChecker  # Ensure this function is implemented

def evaluate_spell_checker(spell_checker, test_data):
    """Evaluate spell checker and display a smooth progress loader."""
    correct_count = 0
    total_bleu = 0
    total_distance = 0
    errors = 0
    smoothing = SmoothingFunction().method1
    total_words = len(test_data)

    print("\n🔍 **Spell Checker Evaluation in Progress...**\n")

    # Initialize tqdm progress bar (tracks count of processed words)
    pbar = tqdm(total=total_words, desc="🔄 Processing", unit="words")

    results_list = []  # Store results for clean output later

    for idx, (misspelled, correct) in enumerate(test_data.items(), start=1):
        suggestions = spell_checker(misspelled)

        if not suggestions:
            errors += 1
            results_list.append((idx, misspelled, "❌ No Suggestion", "-", "-", "❌"))
        else:
            best_bleu = max(sentence_bleu([list(correct)], list(sug), smoothing_function=smoothing) for sug in suggestions)
            total_bleu += best_bleu

            min_distance = min(levenshtein_distance(correct, sug) for sug in suggestions)
            total_distance += min_distance

            is_correct = correct in suggestions
            if is_correct:
                correct_count += 1

            suggestions_str = ", ".join(suggestions[:3])  # Show only first 3 suggestions
            results_list.append((idx, misspelled, suggestions_str, f"{best_bleu:.4f}", min_distance, "✅" if is_correct else "❌"))

        # Update progress bar by one step
        pbar.update(1)
        time.sleep(0.01)  # Tiny delay for smooth effect

    pbar.close()  # Ensure proper cleanup of progress bar

    # Compute final metrics
    accuracy = (correct_count / total_words) * 100 if total_words else 0
    average_bleu = total_bleu / (total_words - errors) if (total_words - errors) else 0
    avg_edit_distance = total_distance / (total_words - errors) if (total_words - errors) else 0

    # Print results after progress completion
    print("\n📌 **Detailed Spell Checker Results**")
    print("=" * 100)
    print(f"{'No.':<5} {'Misspelled Word':<20} {'Suggested Fixes':<40} {'BLEU Score':<12} {'Edit Distance':<15} {'✅ Correct?'}")
    print("=" * 100)

    for result in results_list:
        print(f"{result[0]:<5} {result[1]:<20} {result[2]:<40} {result[3]:<12} {str(result[4]):<15} {result[5]}")

    return {
        "accuracy": accuracy,
        "average_bleu": average_bleu,
        "average_edit_distance": avg_edit_distance,
        "errors": errors
    }

# Load dataset
json_filename = "spell_check_data.json"
with open(json_filename, "r", encoding="utf-8") as f:
    test_data = json.load(f)
test_data = dict(list(test_data.items())[:500])  

# Evaluate spell checker
results = evaluate_spell_checker(triespellChecker, test_data)

# Print final evaluation summary
print("\n📌 **Final Spell Checker Evaluation Results**")
print("=" * 50)
print(f"✅ Accuracy: {results['accuracy']:.2f}%")
print(f"📊 Average BLEU Score: {results['average_bleu']:.4f}")
print(f"✏️  Average Edit Distance: {results['average_edit_distance']:.2f}")
print(f"❌ Errors Encountered: {results['errors']}")
print("=" * 50)

# import requests
# import json

# # URL to Norvig’s Spelling Errors dataset
# DATASET_URL = "https://norvig.com/ngrams/spell-errors.txt"

# def download_and_format_dataset(url):
#     response = requests.get(url)

#     if response.status_code != 200:
#         print("❌ Failed to fetch dataset!")
#         return {}

#     test_data = {}

#     for line in response.text.split("\n"):
#         parts = line.strip().split(": ")
#         if len(parts) == 2:
#             correct_word, incorrect_variants = parts
#             incorrect_words = incorrect_variants.split()  # Split multiple incorrect spellings
#             for incorrect in incorrect_words:
#                 test_data[incorrect] = correct_word  # Store each incorrect spelling

#     return test_data

# # Fetch and format dataset
# test_data = download_and_format_dataset(DATASET_URL)

# # Save as JSON file
# json_filename = "spell_check_data.json"
# with open(json_filename, "w", encoding="utf-8") as f:
#     json.dump(test_data, f, indent=4, ensure_ascii=False)

# print(f"✅ Dataset saved as {json_filename}!")

# # Print sample (first 10 entries)
# for i, (misspelled, correct) in enumerate(test_data.items()):
#     print(f"{i+1}. {misspelled} → {correct}")
#     if i == 9:  # Show only first 10 samples
#         break
