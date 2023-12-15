import pytesseract
from pytesseract import Output
import numpy as np
import pyk4a
from pyk4a import Config, PyK4A
import cv2
import numpy as np
from TTS import tts
import time
# Page segmentation modes: 
# O Orientation and script detection (OSD) only
# 1 Automatic page segmentation with OSD. ‘
# 2 Automatic page segmentation, but no OSD, or OCR.
# 3 Fully automatic page segmentation, but no OSD. (Default)
# 4 Assume a single column of text of variable sizes.
# 5 Assume a single uniform block of vertically aligned text.
# 6 Assume a single uniform block of textJ
# 7 Treat the image as a single text line.
# 8 Treat the image as a single word.
# 9 Treat the image as a single word in a circle.
# 10 Treat the image as a single character.
# 11 Sparse text. Find as much text as possible in no particular order.
# 12 Sparse text with OSD.
# 13 Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract—specific.

# OCR ENGINE MODE
# 0   Legacy engine only
# 1   Neural Nets LSTM engine Only
# 2   LEgacy + LSTM engines
# 3   Default, based on what is available

# tesseract imagename outputbase [-l lang] [--oem ocrenginemode] [--psm pagesegmode] [configfiles...]


def main():
    k4a = PyK4A(
        Config(
            color_resolution=pyk4a.ColorResolution.RES_720P,
            depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
            synchronized_images_only=True,
        )
    )
    k4a.start()

    # getters and setters directly get and set on device
    k4a.whitebalance = 4500
    assert k4a.whitebalance == 4500
    k4a.whitebalance = 4510
    assert k4a.whitebalance == 4510
    time.sleep(1)

    # Get the first frame
    first_frame = None

    while 1:
        capture = k4a.get_capture()
        if first_frame is None and np.any(capture.color):
            first_frame = capture.color[100:500, 200:700, :3]
        
        if np.any(capture.color):
            cv2.imshow("k4a", capture.color[:, :, :3])
            
            cv2.destroyAllWindows()
            break

    k4a.stop()

    # Do something with the first frame (e.g., save it)
    if first_frame is not None:
        cv2.imwrite("sample-text.jpg", first_frame)
        findText()

def findText():
    language = r"eng"
    myconfig = r"--psm 11 --oem 3"
    img = cv2.imread("sample-text.jpg")
    height,width, _ = img.shape
    # boxes = pytesseract.image_to_boxes(img, config=myconfig, output_type=Output.DICT)
    data = pytesseract.image_to_data(img,lang=language, config=myconfig, output_type=Output.DICT)
    accumalated_text = ""
    amount_ofBoxes = len(data['text'])
    for i in range(amount_ofBoxes):
        if float(data['conf'][i])>60:
            print(data['text'][i], data['conf'][i])
            accumalated_text += f"{data['text'][i]} "
        # box = box.split(" ")
            (x,y,width,height) = (data['left'][i],data['top'][i],data['width'][i],data['height'][i])
            img = cv2.rectangle(img,  (x,y),(x+width, y+height), (0,255,0),2)
            img = cv2.putText(img, data['text'][i], (x,y+height+20),cv2.FONT_HERSHEY_COMPLEX, 0.7,(0,255,0),2,cv2.LINE_AA)
    
    print(accumalated_text)
    if len(accumalated_text)>0:
        tts(accumalated_text,"en-US")
    else:
        tts("I can't seem to understand what is written.","en-US")

    cv2.imshow("text", img)
    cv2.waitKey(0)
    # exit(0)

if __name__ == "__main__":
    main()
    # findText()