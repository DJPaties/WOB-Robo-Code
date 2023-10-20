# import cv2
# from objectLogic import analyze_image

# # Initialize the camera
# cap = cv2.VideoCapture(0)
# x, y, width, height = 300, 000, 700, 700  # Example values, adjust these as needed


# ret, frame = cap.read()
# frame_height = frame.shape[0]


# # Crop the frame to the ROI
# frame = frame[y:y+height, x:x+width]
# # Display the camera preview

# # cv2.imshow('Camera Preview', frame)
# if ret:
#     # Save the screenshot as "screenshot.png"
#     cv2.imwrite('sample.png', frame)
#     print("Screenshot saved as 'screenshot.png'")
#     analyze_image()

# # Release the camera and close all OpenCV windows
# cap.release()
# cv2.destroyAllWindows()

import cv2
import numpy as np
from objectLogic import analyze_image
import pyk4a
from pyk4a import Config, PyK4A


import cv2
import numpy as np
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

    # Get the first frame
    first_frame = None

    while 1:
        capture = k4a.get_capture()
        if first_frame is None and np.any(capture.color):
            first_frame = capture.color[:, :, :3]

        if np.any(capture.color):
            cv2.imshow("k4a", capture.color[:, :, :3])
            
            cv2.destroyAllWindows()
            break

    k4a.stop()

    # Do something with the first frame (e.g., save it)
    if first_frame is not None:
        cv2.imwrite("sample.png", first_frame)
        analyze_image()

if __name__ == "__main__":
    main()
