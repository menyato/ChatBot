import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from gen_wav import to_wav

def chat(sentence):
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


    intents_path = r'intents.json'

    with open(intents_path, 'r', encoding='utf-8') as json_data:
        intents = json.load(json_data)

    FILE = r"data.pth"
    data = torch.load(FILE)  #


    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]

    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()
    

    bot_name = "Teacher"
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
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
                    to_wav(x)
                    return x 

        else:
            print(f"{bot_name}: I do not understand ")
            return "Your response is not available " , to_wav("I do not know this question")
            # ask_questions(sentence)