from googletrans import Translator
import re
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk 
nltk.download('punkt')

nltk.download('maxent_ne_chunker')
nltk.download('words')
translator = Translator()
def get_name(sentence):    

    if "إسمي" in sentence:
        print(" Found")
    else:
        sentence = "اسمي " + sentence
    translation = translator.translate(sentence, src='ar', dest='en')
    translated =  translation.text
    # input_sentence = "my name is ahmad ibrahim"
    print(translated)
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
    return names[0]
# while True:
#     inp = input("")
#     print(get_name(inp))
# get_name("عبد فواز")


