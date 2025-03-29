from transformers import T5ForConditionalGeneration, T5Tokenizer

tokenizer = T5Tokenizer.from_pretrained("t5-small", legacy=True)
model = T5ForConditionalGeneration.from_pretrained("t5-small")

def t5_spell_correct(sentence):
    input_text = f"fix: {sentence}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    output_ids = model.generate(input_ids)
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

print(t5_spell_correct("eduction"))  # "This is a spelling error."
