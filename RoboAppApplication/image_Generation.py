from openai import OpenAI
from ExtraTTS import tts
from ExtraMicrophone import stt
import cv2
import numpy as np
from googletrans import Translator


translator = Translator()
msg = "سفينه التايتنك عم تضرب بالثلج"
translation = translator.translate(msg, src='ar', dest='en')
translated =  translation.text
print(translated)

