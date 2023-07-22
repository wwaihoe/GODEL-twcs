from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

#Initialize tokenizer and model
model_name = "GODEL_twcs"

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
    outputs = model.generate(input_ids, max_length=128, min_length=8, top_p=0.9, do_sample=True)
    output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return output

# Instruction for a chitchat task
instruction = f"Instruction: given a dialog context, provide a helpful response."
# Leave the knowldge empty
knowledge = ""
dialog = []

while(True):
    dialog.append(input("Enter dialog: "))
    if dialog[-1] == "exit()":
        break
    if dialog[-1] == "reset()":
        dialog = []
        print('new conversation started...')
        continue
    generated_text = generate(instruction, knowledge, dialog)
    dialog.append(generated_text)
    print("GODEL: " + generated_text)