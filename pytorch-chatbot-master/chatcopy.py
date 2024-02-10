import random
import json
import torch
import os
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
import requests
from flask import Flask, request
import time
from sentence_transformers import SentenceTransformer, util
import chatgpt
import serial


app = Flask(__name__)
global run_once
run_once = True
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
all_patterns = ["سام هيدا مش اسمي","هيدا مش اسمي","you got my name wrong","you said my name wrong","Sam you said my name wrong","Sam you got my name wrong",
                "أنا شاب ولا بنات","أنا صبي ولا بنت"," سام أنا شاب ولا بنات","سام أنا صبي ولا بنت","شو للجندر تعوله","شو الجندر تعوله سام","سام شو الجندر تعوله",
                "What is my mood","Can you see my facial expressions","Sam can you see my mood","Sam what are my facial expressions","Can you feel my mood",
                "Can you guess my gender","What is my gender?"," Sam what is my gender","Sam am i a boy or girl","Sam am i a girl or boy","Sam am i a man or woman","Sam am i a woman or man",
                "فيك تشوف تعابير وجهي","يَلَّا حُطْ وِجَّكْ لَ شُوفْ تَعَبِيرُ",'فيك تركز على إيدي', 'هات نشوف اذا  فيك تركزعلى ما أقول', 'هات نشوف اذا  فيك تركزعلي ', 'سام خلينا نشوف تركيزك', 
                'سام، يلا نلعب لعبة التركيز', 'بدي ورجيك هلا شيء وانت قل لي شو لونه', 'فيك تقول لي شو لونه هيدا', 'شو لونه هيدا', 
                'شو هيدا اللون', 'ممكن تحكيلي شو لونو', 'اعطيني لونو، بدي اعرف', 'اعطيني لونو', 'شوفي مكتوب هان', 'شوفي مكتوب هون', 
                'فيك تقرا هاالكلمة', 'فيك تشوف شو مكتوب هون', 'فيك تقرا شو مكتوب', 'شكرًا على مساعدتك', 'شكرًا', 'شكرًا جزيلاً لك', 
                'أنت الأفضل', 'قل لي نكتة', 'عطيني نكتة', 'اعطيني نكته', 'تعا ناخد سلفي', 'تعال ناخد سيلفي', 'فيك تعمل لايك', 
                'عمول لايك', 'عمال لايك', 'علّي أيدك اليمين', 'ارفع أيدك اليمين', 'علي ايدك اليمين', 'علّي أيدك الشمال', 
                'علّي أيدك اليسار', 'علي ايدك لشمال', 'ارفع أيدك الشمال', 'ارفع أيدك اليسار', 'علي ايدك', 'ارفع أيدك', 'قلدني', 
                'عمال متلي', 'ماسك بأيدي', 'هل تعرف هذا الشيء', 'شو في بأيدي', 'أدي المسافة بيني وبينك', ' أديش المسافة بيني وبينك', 
                'أديش ببعد عنك', 'قديه مسافه بيني وبينك', 'يلا نلعب جاك', 'وقت اللعب يا جاك', 'حان وقت لعبة الحجر والمقص والورق',
                'ما رأيك في لحيتي', 'شو رأيك بدقني حلوى', 'دقني حلوة شي', 'كم إصبعًا لدي مرفوع', 'كم أصبع أنا رافع',
                'هل يمكنك عد الأصابع التي أرفعها', 'خمسة زائد سبعة', 'سبعة زائد خمسة', '5 + 7', 'ثلاثة زائد أربعة', 'أربعة زائد ثلاثة', 
                '4 + 3', 'أنا مش منيح', 'أنا مني منيح', 'مني بخير', 'الحمد لله', 'منيح', 'أنا منيح', 'تمام لحمدلله', 
                'كنت حابة أبقى معك أكتر بس خلصت المقابلة ونبسطت أنو تعرفت عليك وعلى الأشياءالحلوة لي بتعمل', 'نبسطت معنا اليوم ', 
                'فيك تعرف العالم لي قدامك', 'فيك تتعرف على العالم', 'شو فيك تفرجينا بعد زيادة', 'شو فيك تفرجينا بعد', 
                'قلتلي أنو فيك تلعب معي', 'خبرتني أنو فينا نلعب أدمك', 'طيب مين المبرمجين لي شتغلو عليك', 'مين المبرمجين لي عملوك', 
                'عرفنا على الناس لي برمجوك', 'عرفنا على الناس اللي برمج', 'ناس اللي برمج', 'مين المبرمجين اللي اشتغلوا عليك', 
                'مين المبرمجين اللي اشتغلوا على كام', 'طيب مين هيدول العالم فيك تعرفناعليهون', 'مين هيدول العالم', 'عرفنا على العالم', 
                'طيب ما قلتلنا كيف أقدرت تصير تعمل هيك', 'كيف أقدرت تصير تعمل هيك', 'طيب شو حنبلش نشوف', 'شو حنشوف', 
                'طيب شو حانبلش نشوف', 'عرفنا عن حالك', 'مين أنت', 'أنت مين', 'شو جاي تعمل اليوم', 'شو بدك تورجينا', 'شو حاتعمل اليوم',
                'شو حاتفرجينا اليوم', 'مرحبا كيفك', 'كيفك', 'Hi', 'Hey', 'How are you', 'Is anyone there?', 'Hello', 'Good day', 'Bye', 
                'See you later', 'Goodbye', "Jack isn't it", 'Alright jack, how tall are you', 'how tall are you', 'what is your height', 
                "that's the perfect height for a man", 'perfect height for a man', 'you have a perfect height', 'wow you are tall', 
                "that's why I'm pleased to have you here jack", 'I know you are perfect that is why im pleased to have you here', 
                'I am pleased to have you here', "seems like you've got special abilities, what can you do Jack", 
                'its like you got special abilites', 'What can you do Jack', 'So what are the services', 'What services do you provide', 
                'What can you provide for us services', 'Sure, I can hear that', 'I can for sure hear that', 'I can hear that for sure', 
                'I see you laugh, so do you have feelings', 'So do you have feelings', 'If you can laugh then you have feelings right', 
                'Well seems like there are a lot of technologies in there', 'It seems like you have lot of technology in you',
                'It seems like you have lot of technology in there', 'you have lot of technology in there', 'I see you have lots of techology', 
                "so you've got some opinions about humans", 'Opinion on humans', 'have you ever been in a relationship with humans', 
                'did you have relationship with humans', 'relationship with humans', "You said you don't have feelings though, how is that", 
                "you just told me you didn't have feelings", "how can't feel how is that", 
                "you're so funny Jack, can you tell us what you usually do in your day", 'what you usually do in your day', 
                'tell us how do you spend your day', 'how do you usually spend your day', 
                "You've got a lot of self-confidence, who has taught you this too", 'you are confident who taught you this.', 
                'who taught you that confidence', 'Thats actually correct, I would like to thank World of Business team', 
                'Thank you World of business for making Jack', 'Thanks for World of Business for this masterpiece', 
                'sure man, enjoy your time', 'Go ahead enjoy your time', 'Go ahead have fun', 'Can you read what is written here', 
                'Can you read this word', 'what is this word', 'Can you understand what this says', 'Are you able to read this text', 
                'Do you know what this word says', 'Can you see what is this color', 'What is this color', 'Name this', 'Sam what is this color',
                'Sam name this color', 'Can you tell me the name of this color', 'tell the name of this color', 'Can you focus on my hand', 
                "Let's see if you can focus on what i say", "Let's see if you can focus", "Sam let's see you focus", "Sam let's play focus game",
                'Can you track my hand']
#load the comparison model
api_token ="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"
API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/paraphrase-MiniLM-L6-v2"
# API_URL = API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {api_token}"}

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        
    except ValueError as e:
        print(e)

    return response.json()

device = torch.device('cuda')#if torch.cuda.is_available() else 'cpu')

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

embedder = SentenceTransformer('all-MiniLM-L6-v2').to(device)
corpus_embeddings = embedder.encode(all_patterns, convert_to_tensor=True).to(device)
def search(msg):    
    # Query sentences:
    queries = [msg]


    # Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
    top_k = min(1, len(all_patterns))
    for query in queries:
        query_embedding = embedder.encode(query, convert_to_tensor=True)

        # We use cosine-similarity and torch.topk to find the highest 5 scores
        cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
        top_results = torch.topk(cos_scores, k=top_k)

        for score, idx in zip(top_results[0], top_results[1]):
            print(all_patterns[idx], "(Score: {:.4f})".format(score))
            
        print(all_patterns[idx])
        return all_patterns[idx], "{:.4f}".format(score)

 

@app.route('/receive', methods=['POST'])
def receive_message():
    
    sentenceinput = request.json.get('message','')

    print(f"Received message from user: {sentenceinput}")
    print(sentenceinput)
    if sentenceinput == "quit":
        exit()
    print("enter query")
    try:
        data, score = search(sentenceinput)
        if float(score)<0.9:
            response = chatgpt.chat(sentenceinput)
            
            return response
        sentence = data
        print(sentence)
        
    except ValueError as e:
        print(e)
        
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
        # print(prob.item())
        for intent in intents['intents']:
            if tag == intent["tag"]:
                print(f"{intent['tag']}")
                x = (f"{random.choice(intent['responses'])}")
                print(x)
                message = {
                    "text": x,
                    "intent": intent['tag']
                }
                data = json.dumps(message)
                # tts(x,"ar-LB")
                return data
    else:
        print(f"{bot_name}: I do not understand...")
        return f"{bot_name}: I do not understand..."

# if run_once:
#     receive_message()


    



if __name__ == '__main__':
    app.run(port=5000)