import random
import json
import torch
import os
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
import requests
#load the text:
# Get the current script directory
script_dir = os.path.dirname(__file__)
json_path = os.path.join(script_dir, 'intents.json')

# Load JSON data from file
with open(json_path, 'r',encoding='utf-8') as file:
    data = json.load(file)

# Extract and print patterns
# all_patterns = []
# for intent in data['intents']:
#     all_patterns.extend(intent['patterns'])
# print(all_patterns)
all_patterns = ['شكرًا على مساعدتك', 'شكرًا', 'شكرًا جزيلاً لك', 'أنت الأفضل', 'قل لي نكتة', 'عطيني نكتة', 'تعا ناخد سلفي', 
                          'فيك تعمل لايك', 'عمول لايك', 'عمال لايك', 'علّي أيدك اليمين', 'ارفع أيدك اليمين', 'علّي أيدك الشمال', 
                          'علّي أيدك اليسار', 'ارفع أيدك الشمال', 'ارفع أيدك اليسار', 'علي ايدك', 'ارفع أيدك', 'قلدني', 'عمال متلي', 
                          'ماسك بأيدي', 'هل تعرف هذا الشيء', 'شو في بأيدي', 'أدي المسافة بيني وبينك', ' أديش المسافة بيني وبينك', 
                          'أديش ببعد عنك', 'يلا نلعب جاك', 'وقت اللعب يا جاك', 'حان وقت لعبة الحجر والمقص والورق', 'ما رأيك في لحيتي', 
                          'شو رأيك بدقني حلوى', 'دقني حلوة شي', 'كم إصبعًا لدي مرفوع', 'كم أصبع أنا راف       فع', 'هل يمكنك عد الأصابع التي أرفعها',
                            'خمسة زائد سبعة', 'سبعة زائد خمسة', '5 + 7', 'ثلاثة زائد أربعة', 'أربعة زائد ثلاثة', '4 + 3', 'أنا مش منيح', 'أنا مني منيح', 
                            'مني بخير', 'الحمد لله', 'منيح', 'أنا منيح', 'تمام لحمدلله', 
                            'كنت حابة أبقى معك أكتر بس خلصت المقابلة ونبسطت أنو تعرفت عليك وعلى الأشياءالحلوة لي بتعمل', 'نبسطت معنا اليوم ', 
                            'فيك تعرف العالم لي قدامك', 'فيك تتعرف على العالم', 'شو فيك تفرجينا بعد زيادة', 'شو فيك تفرجينا بعد', 'قلتلي أنو فيك تلعب معي',
                              'خبرتني أنو فينا نلعب أدمك', 'طيب مين المبرمجين لي شتغلو عليك', 'مين المبرمجين لي عملوك', 'عرفنا على الناس لي برمجوك', 
                              'طيب مين هيدول العالم فيك تعرفناعليهون', 'مين هيدول العالم', 'عرفنا على العالم', 'طيب ما قلتلنا كيف أقدرت تصير تعمل هيك',
                                'كيف أقدرت تصير تعمل هيك', 'طيب شو حنبلش نشوف', 'شو حنشوف', 'طيب شو حانبلش نشوف', 'عرفنا عن حالك', 'مين أنت', 'أنت مين',
                                  'شو جاي تعمل اليوم', 'شو بدك تورجينا', 'شو حاتعمل اليوم', 'شو حاتفرجينا اليوم', 'مرحبا كيفك', 'كيفك', 
                                  'Hi', 'Hey', 'How are you', 'Is anyone there?', 'Hello', 'Good day', 'Bye', 'See you later', 'Goodbye']
#load the comparison model
api_token ="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"
API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/paraphrase-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {api_token}"}

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
    except ValueError as e:
        print(e)

    return response.json()

device = torch.device('cuda' )#if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r', encoding="utf8") as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"
print("Let's chat! (type 'quit' to exit)")
while True:
    # sentence = "do you use credit cards?"
    print("start")
    # sentenceinput = stt()
    sentenceinput = input(">")

    print(sentenceinput)
    if sentenceinput == "quit":
        break
    print("enter query")
    try:
        data = query(
            {
                "inputs": {
                    "source_sentence": f"{str(sentenceinput)}",
                    "sentences":['شكرًا على مساعدتك', 'شكرًا', 'شكرًا جزيلاً لك', 'أنت الأفضل', 'قل لي نكتة', 'عطيني نكتة', 'تعا ناخد سلفي', 
                            'فيك تعمل لايك', 'عمول لايك', 'عمال لايك', 'علّي أيدك اليمين', 'ارفع أيدك اليمين', 'علّي أيدك الشمال', 
                            'علّي أيدك اليسار', 'ارفع أيدك الشمال', 'ارفع أيدك اليسار', 'علي ايدك', 'ارفع أيدك', 'قلدني', 'عمال متلي', 
                            'ماسك بأيدي', 'هل تعرف هذا الشيء', 'شو في بأيدي', 'أدي المسافة بيني وبينك', ' أديش المسافة بيني وبينك', 
                            'أديش ببعد عنك', 'يلا نلعب جاك', 'وقت اللعب يا جاك', 'حان وقت لعبة الحجر والمقص والورق', 'ما رأيك في لحيتي', 
                            'شو رأيك بدقني حلوى', 'دقني حلوة شي', 'كم إصبعًا لدي مرفوع', 'كم أصبع أنا راف       فع', 'هل يمكنك عد الأصابع التي أرفعها',
                            'خمسة زائد سبعة', 'سبعة زائد خمسة', '5 + 7', 'ثلاثة زائد أربعة', 'أربعة زائد ثلاثة', '4 + 3', 'أنا مش منيح', 'أنا مني منيح', 
                            'مني بخير', 'الحمد لله', 'منيح', 'أنا منيح', 'تمام لحمدلله', 
                            'كنت حابة أبقى معك أكتر بس خلصت المقابلة ونبسطت أنو تعرفت عليك وعلى الأشياءالحلوة لي بتعمل', 'نبسطت معنا اليوم ', 
                            'فيك تعرف العالم لي قدامك', 'فيك تتعرف على العالم', 'شو فيك تفرجينا بعد زيادة', 'شو فيك تفرجينا بعد', 'قلتلي أنو فيك تلعب معي',
                            'خبرتني أنو فينا نلعب أدمك', 'طيب مين المبرمجين لي شتغلو عليك', 'مين المبرمجين لي عملوك', 'عرفنا على الناس لي برمجوك', 
                            'طيب مين هيدول العالم فيك تعرفناعليهون', 'مين هيدول العالم', 'عرفنا على العالم', 'طيب ما قلتلنا كيف أقدرت تصير تعمل هيك',
                            'كيف أقدرت تصير تعمل هيك', 'طيب شو حنبلش نشوف', 'شو حنشوف', 'طيب شو حانبلش نشوف', 'عرفنا عن حالك', 'مين أنت', 'أنت مين',
                            'شو جاي تعمل اليوم', 'شو بدك تورجينا', 'شو حاتعمل اليوم', 'شو حاتفرجينا اليوم', 'مرحبا كيفك', 'كيفك', 
                            'Hi', 'Hey', 'How are you', 'Is anyone there?', 'Hello', 'Good day', 'Bye', 'See you later', 'Goodbye']
        }
            })
        print(type(data))
        sentence = (all_patterns[data.index(max(data))])
    except ValueError as e:
        print(e)
        continue
    print("after data")
    sentence = tokenize(sentence)
    print("Tokenize")
    print(sentence)
    # sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    
    if prob.item() > 0.75:
        print(prob.item())
        for intent in intents['intents']:
            if tag == intent["tag"]:
                print(f"{intent['tag']}")
                x = (f"{random.choice(intent['responses'])}")
                print(x)
                # tts(x,"ar-LB")
    else:
        print(f"{bot_name}: I do not understand...")