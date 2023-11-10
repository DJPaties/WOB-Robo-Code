import cv2
import numpy as np
import pyk4a
from pyk4a import Config, PyK4A
import mediapipe as mp
import cv2 
def main():
    k4a = PyK4A(
        Config(
            color_resolution=pyk4a.ColorResolution.RES_720P,
            depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
            synchronized_images_only=True,
        )
    )
    k4a.start()
    mp_Hands = mp.solutions.hands
    hands = mp_Hands.Hands()
    mpDraw = mp.solutions.drawing_utils
    finger_Coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
    thumb_Coord = (4,2)
    # getters and setters directly get and set on device
    k4a.whitebalance = 4500
    assert k4a.whitebalance == 4500
    k4a.whitebalance = 4510
    assert k4a.whitebalance == 4510

    while 1:
        capture = k4a.get_capture()
        if np.any(capture.color):
            # Define the coordinates of the region you want to capture
            # In this example, we're cropping a region from (100, 100) to (500, 500)
            x1, y1, x2, y2 = 500, 000, 1000, 800
            cropped_image = capture.color[y1:y2, x1:x2, :3]
            RGB_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
            results = hands.process(RGB_image)
            multiLandMarks = results.multi_hand_landmarks
            if multiLandMarks:
                handList = []
                for handLms in multiLandMarks:
                    print(handLms)
                    mpDraw.draw_landmarks(cropped_image, handLms, mp_Hands.HAND_CONNECTIONS)
                    for idx, lm in enumerate(handLms.landmark):
                        h, w, c = cropped_image.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                    handList.append((cx, cy))
                for point in handList:
                    cv2.circle(cropped_image, point, 10, (255, 255, 0), cv2.FILLED)
                upCount = 0
            cv2.imshow("k4a", cropped_image)
            key = cv2.waitKey(10)
            if key != -1:
                cv2.destroyAllWindows()
                break
    k4a.stop()

if __name__ == "__main__":
    main()
