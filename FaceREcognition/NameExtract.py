from translate import Translator
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk

translator = Translator(from_lang="ar",to_lang='en')  # Specify the target language during initialization

def get_name(sentence, languagecode):
    translated =""
    if languagecode == "en-US":
        if "My name is" in sentence:
            translated =  sentence
        else:
            translated = "My name is " + sentence
    else:
        if "إسمي" in sentence or "أنا اسمي" in sentence:
            print(" Found")
        else:
            sentence = "اسمي " + sentence

        translation = translator.translate(sentence)
        translated = translation
    # translated = translated.replace("-", "")
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
    if not names:
        return ""
    return names[0]

# get_name(" أنا اسمي محمد دغيلي", "ar-LB")
# x = get_name("My name is Mohammed Al-Deghaili", "en-US")
# print(len(x))