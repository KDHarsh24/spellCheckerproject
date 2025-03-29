from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load Pretrained Model
model_name = "google/t5-v1_1-small"
tokenizer = T5Tokenizer.from_pretrained(model_name, legacy=False)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def correct_spelling(sentence):
    """Fix spelling mistakes using the T5 model."""
    input_text = f"fix spelling: {sentence}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    # Generate corrected text
    output_ids = model.generate(input_ids, max_length=64, num_return_sequences=1)
    corrected_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return corrected_text

# Example Usage
sentence = "exampl"
corrected_sentence = correct_spelling(sentence)

print("Original:", sentence)
print("Corrected:", corrected_sentence)
