import json
import requests
import speech_recognition as sr 
import time
import os
from google.cloud import texttospeech
import pygame
import glob
import time
from mutagen.mp3 import MP3
import wave
from concurrent.futures import ThreadPoolExecutor
from serialSender import mouth, talking_scenario


def send_message(msg):

    
    print(msg)
    url = 'http://127.0.0.1:5000/receive'
    data = {'message': msg}
    response = requests.post(url, json=data)
    data = response.json()
    print(data)
    # if data['message'] == False:
    #     time.sleep(1)
    #     send_message(data['intent'])
    # else:
    return (data)

    # payload = {

    #                 "sender": "user1",
    #                 "message": msg
    #             }
    # print("Payload done")
    # # r = requests.post('http://localhost:5005/webhook/rest/webhook', json=payload)
    # # r = requests.post('http://f516-185-127-125-53.ngrok.io/webhooks/rest/webhook', json=payload)
    # r = requests.post('http://127.0.0.1:5000/chat',json=payload)
    # print("Request done")
    # # data = r.json()
    # data = r.json()
    # print(data)
    # Process the response from the Rasa chatbot
    # response = None
    # for message in data:

    #     response = message["text"]
    # # print("Enter try")
    # try:
    #     return_Message = json.loads(response)
    #     x = (return_Message)
    #     print(x)
    #     return return_Message
    # except ValueError as e :
    #     # print("Response is not a json")

    #     print(response)
    #     return response


# send_message("What is the mass of the sun")
