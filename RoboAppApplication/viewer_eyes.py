import cv2
import numpy as np
from serialSender import talking_scenario
import pyk4a
from pyk4a import Config, PyK4A

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
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    while 1:
        capture = k4a.get_capture()
        if np.any(capture.color):
            gray = cv2.cvtColor(capture.color[:,:,:3], cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5,minSize=(30,30))
            for (x, y, w, h) in faces: 
                cv2.rectangle(capture.color, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green rectangle around the face
                center = (x + w // 2, y + h // 2)
                radius = 4
                cv2.circle(capture.color, center, radius, (0, 0, 255), 2)  # Red circle in the center of the face
                print(center[0])
                if center[0]>=950:
                    talking_scenario(5,"any", "#20P1300\r\n")
                elif center[0]>=800:
                    talking_scenario(5,"any", "#20P1350\r\n")
                elif center[0]>=600:
                    talking_scenario(5,"any", "#20P1400\r\n")
                elif center[0]>=500:
                    talking_scenario(5,"any", "#20P1450\r\n")
                elif center[0]>=400:
                    talking_scenario(5,"any", "#20P1500\r\n")
                elif center[0]>=300:
                    talking_scenario(5,"any", "#20P1550\r\n") 
                elif center[0]>=200 :  
                    talking_scenario(5,"any", "#20P1600\r\n")
                elif center[0]>=100 :  
                    talking_scenario(5,"any", "#20P1650\r\n")
            cv2.imshow("k4a", capture.color[:, :, :3])
            key = cv2.waitKey(10)
            if key != -1:
                cv2.destroyAllWindows()
                break
    k4a.stop()


if __name__ == "__main__":
    main()



