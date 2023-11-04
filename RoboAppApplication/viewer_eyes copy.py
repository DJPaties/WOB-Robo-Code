import cv2
import numpy as np
from serialSender import talking_scenario
import pyk4a
from pyk4a import Config, PyK4A
import time

global signal
signal = True

def set_signal(boolean):
    global signal
    signal = boolean

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
    global code
    code = ""
    global new_code
    new_code = ""
    global face_code
    face_code = ""
    face_counter = 0

    while 1:
        if signal == False:
            break

        capture = k4a.get_capture()

        if np.any(capture.color):
            gray = cv2.cvtColor(capture.color[:, :, :3], cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
            # print(faces)
            
            # Update the face detection counter
            face_counter = len(faces)

            for (x, y, w, h) in faces:
                cv2.rectangle(capture.color, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green rectangle around the face
                center = (x + w // 2, y + h // 2)
                radius = 4
                cv2.circle(capture.color, center, radius, (0, 0, 255), 2)  # Red circle in the center of the face
                # print(center[0])
                if center[0] >= 950:
                    new_code = "#20P1300\r\n"
                    face_code = "#16P1600T500D500\r\n"
                elif center[0] >= 800:
                    # 1550
                    new_code = "#20P1350\r\n"
                    face_code = "#16P1550T500D500\r\n"
                elif center[0] >= 600:
                    # 1550
                    new_code = "#20P1400\r\n"
                    face_code = "#16P1500T500D500\r\n"
                    time.sleep(0.2)
                elif center[0] >= 500:
                    new_code = "#20P1450\r\n"
                    face_code = "#16P1450T500D500\r\n"
                elif center[0] >= 400:
                    new_code = "#20P1500\r\n"
                    face_code = "#16P1400T500D500\r\n"
                elif center[0] >= 300:
                    new_code = "#20P1550\r\n"
                    face_code = "#16P1350T500D500\r\n"
                elif center[0] >= 200:
                    new_code = "#20P1600\r\n"
                    face_code = "#16P1300T500D500\r\n"
                elif center[0] >= 100:
                    new_code = "#20P1650\r\n"
                    face_code = "#16P1250T500D500\r\n"
                # print(new_code, code)
                if new_code != code:
                    code = new_code
                    try:
                        talking_scenario(5, 'any', new_code)
                        time.sleep(0.2)
                        talking_scenario(5, 'any', face_code)
                    except ValueError as e:
                        print(e)
                        pass
                time.sleep(0.1)

        # Display the face detection counter on the frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(capture.color, f'Faces: {face_counter}', (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("k4a", capture.color[:, :, :3])
        key = cv2.waitKey(10)
        if key != -1:
            cv2.destroyAllWindows()
            break

    k4a.stop()

if __name__ == "__main__":
    main()
# import cv2
# import numpy as np
# from serialSender import talking_scenario
# import pyk4a
# from pyk4a import Config, PyK4A
# import time

# global signal
# signal = True

# def set_signal(boolean):
#     global signal
#     signal = boolean

# def main():
#     k4a = PyK4A(
#         Config(
#             color_resolution=pyk4a.ColorResolution.RES_720P,
#             depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
#             synchronized_images_only=True,
#         )
#     )
#     k4a.start()

#     # getters and setters directly get and set on device
#     k4a.whitebalance = 4500
#     assert k4a.whitebalance == 4500
#     k4a.whitebalance = 4510
#     assert k4a.whitebalance == 4510
#     face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#     global code
#     code = ""
#     global new_code
#     new_code = ""
#     global face_code
#     face_code = ""
#     face_detected = False

#     while 1:
#         if signal == False:
#             break

#         capture = k4a.get_capture()

#         if np.any(capture.color):
#             gray = cv2.cvtColor(capture.color[:, :, :3], cv2.COLOR_BGR2GRAY)
#             faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
            
#             # If faces are detected, track the most prominent face
#             # ...
#             if len(faces) > 0:
#                 x, y, w, h = max(faces, key=lambda face: (face[2] * face[3]))
#                 cv2.rectangle(capture.color, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green rectangle around the face
#                 center = (x + w // 2, y + h // 2)
#                 radius = 4
#                 cv2.circle(capture.color, center, radius, (0, 0, 255), 2)  # Red circle in the center of the face


#                 if center[0] >= 950:
#                     new_code = "#20P1300\r\n"
#                     face_code = "#16P1600\r\n"
#                 elif center[0] >= 800:
#                     # 1550
#                     new_code = "#20P1350\r\n"
#                     face_code = "#16P1550\r\n"
#                 elif center[0] >= 600:
#                     # 1550
#                     new_code = "#20P1400\r\n"
#                     face_code = "#16P1500\r\n"
#                     time.sleep(0.2)
#                 elif center[0] >= 500:
#                     new_code = "#20P1450\r\n"
#                     face_code = "#16P1450\r\n"
#                 elif center[0] >= 400:
#                     new_code = "#20P1500\r\n"
#                     face_code = "#16P1400\r\n"
#                 elif center[0] >= 300:
#                     new_code = "#20P1550\r\n"
#                     face_code = "#16P1350\r\n"
#                 elif center[0] >= 200:
#                     new_code = "#20P1600\r\n"
#                     face_code = "#16P1300\r\n"
#                 elif center[0] >= 100:
#                     new_code = "#20P1650\r\n"
#                     face_code = "#16P1250\r\n"

#                 print(new_code, code)
#                 if new_code != code:
#                     code = new_code
#                     try:
#                         talking_scenario(5, 'any', new_code)
#                         time.sleep(0.2)
#                         talking_scenario(5, 'any', face_code)
#                     except ValueError as e:
#                         print(e)
#                         pass

#                 face_detected = True
#             else:
#                 face_detected = False

#         # Display the face detection status on the frame
#         if face_detected:
#             status_text = "Face Detected"
#         else:
#             status_text = "No Face Detected"
#         font = cv2.FONT_HERSHEY_SIMPLEX
#         cv2.putText(capture.color, status_text, (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

#         cv2.imshow("k4a", capture.color[:, :, :3])
#         key = cv2.waitKey(10)
#         if key != -1:
#             cv2.destroyAllWindows()
#             break

#     k4a.stop()

# if __name__ == "__main__":
#     main()
