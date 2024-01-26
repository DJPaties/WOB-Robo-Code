from googletrans import Translator
import re
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk 

nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('averaged_perceptron_tagger')
translator = Translator()
def get_name(sentence,languagecode):    
    if languagecode == "en-US":
        if "My name is" in sentence:
            pass
        else:
            translated= "My name is "+sentence
    else:
        if "إسمي" in sentence or "أنا اسمي" in sentence:
            print(" Found")
        else:
            sentence = "اسمي " + sentence
    
        translation = translator.translate(sentence, src='ar', dest='en')
        translated =  translation.text
        print(translated)
    # print(sentence)
    # input_sentence = "my name is ahmad ibrahim"
        
    tokens = word_tokenize(translated)

    tagged_tokens = pos_tag(tokens)

    named_entities = ne_chunk(tagged_tokens)

    names = []
    for entity in named_entities:
        if isinstance(entity, nltk.Tree):
            if entity.label() == 'PERSON':
                name = ' '.join([word for word, tag in entity.leaves()])
                names.append(name)
    print(names)
    if names == []:
        names = ''
        if not names:
            print("YES")
        return ""
    return names[0]
# while True:
#     inp = input("")
#     print(get_name(inp))
# get_name("عبد فواز","ar-LB")


# get_name(" أنا اسمي محمد دغيلي","ar-LB")




