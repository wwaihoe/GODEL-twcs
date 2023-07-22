from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = 'GODEL_twcs'

#Initialize tokenizer and model
print(f"loading model {model_name}...", end='', flush=True)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
print("completed")

#generate function for GODEL
def generate(instruction, knowledge, dialog):
    if knowledge != '':
        knowledge = '[KNOWLEDGE] ' + knowledge
    dialog = ' EOS '.join(dialog)
    query = f"{instruction} [CONTEXT] {dialog} {knowledge}"
    input_ids = tokenizer(f"{query}", return_tensors="pt").input_ids
    try:
        outputs = model.generate(input_ids, max_length=128, min_length=8, top_p=0.9, do_sample=True)
        output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    except:
        output = f'Error with model'
    return output

