from openai import OpenAI
import cv2
import numpy as np
# tts("Give me a description for the image you would like to see","en-US")
# msg = stt("en-US")

# tts("Let me have a minute so i can draw it for you","en-US")

client = OpenAI(api_key="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")
msg="سفينه التايتنك عم تضرب بالثلج"
def image_gen(msg):
  response = client.images.generate(
    model="dall-e-2",
    prompt=msg,
    size="512x512",
    quality="standard",
    n=1,
  )

  image_url = response.data[0].url
  print(image_url
        )
  import requests

  url = image_url
  response = requests.get(url)

  # with open("image.jpg", "wb") as f:
  #     f.write(response.content)
  image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
  image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

  cv2.imwrite("generated_image.jpg", f"C:/Users/WOB/Desktop/WOB-Robo-Code-main/RoboAppApplication/{image}")

