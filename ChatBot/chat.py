import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from openai_pdf import ask_questions

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Specify the correct file path for your intents file
intents_path = r'intents.json'

with open(intents_path, 'r', encoding='utf-8') as json_data:
    intents = json.load(json_data)

FILE = r"data.pth"
data = torch.load(FILE)  # Use FILE instead of intents

# Rest of your code remains unchanged...


input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Lawyer"
print("Let's chat! (type 'quit' to exit)")
while True:
    # sentence = "do you use credit cards?"
    sentence = input("You: ")
    if sentence == "quit":
        break

    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
         for intent in intents['intents']:
            if tag == intent["tag"]:
                #print(f"{intent['tag']}")
                x = (f"{random.choice(intent['responses'])}")
                print(x)

    else:
        print(f"{bot_name}: I do not understand I am retrieving the content from the pdf")
        ask_questions(sentence)