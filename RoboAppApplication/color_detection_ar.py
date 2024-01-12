import numpy as np
import pyk4a
from pyk4a import Config, PyK4A
import cv2
import numpy as np
import time
import pandas as pd
from collections import Counter
from TTS import tts
import random
color_data = pd.read_csv('arabiccolorsexcel.csv')

def get_color_name(b, g, r):
    # Find the closest match based on Euclidean distance
    color_data['distance'] = ((color_data['Red (8 bit)'] - r) ** 2 + (color_data['Green (8 bit)'] - g) ** 2 + (color_data['Blue (8 bit)'] - b) ** 2) ** 0.5
    closest_color = color_data.loc[color_data['distance'].idxmin(), 'Arabic Name']
    # closest_color = closest_color.split("!")
    
    return closest_color



def main():
    frame_count = 0
    color_counter = Counter()
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

    while frame_count < 50:
        capture = k4a.get_capture()

        if np.any(capture.color):
            frame = capture.color[:, :, :3]  # Extract the BGR frame
            # cv2.imshow("k4a", frame)

            pixel_center_bgr = frame[int(frame.shape[0] / 2), int(frame.shape[1] / 2)]
            b, g, r = map(int, pixel_center_bgr)

            color = get_color_name(b, g, r)
            color_counter[color] += 1

            # Create a copy of the frame for drawing
            frame_with_drawings = frame.copy()

            cv2.rectangle(frame_with_drawings, (frame.shape[1] // 2 - 220, 10), (frame.shape[1] // 2 + 200, 120), (255, 255, 255), -1)
            cv2.putText(frame_with_drawings, color, (frame.shape[1] // 2 - 200, 100), 0, 1, (b, g, r), 5)
            cv2.circle(frame_with_drawings, (frame.shape[1] // 2, frame.shape[0] // 2), 5, (25, 25, 25), 3)

            cv2.imshow("k4a_with_drawings", frame_with_drawings)

            frame_count += 1

        key = cv2.waitKey(1)
        if key == 27:  # Press 'Esc' key to exit the loop
            break

    # Find the color with the highest frequency
    most_common_color = color_counter.most_common(1)[0][0]
    print(f"Most common color: {most_common_color}")

    k4a.stop()
    cv2.destroyAllWindows()
    random_answsers = ["انا شايف  ", "يِمْكِنْ هَيْدَا ","هِمْمْمْ يِمْكِنْ هَيْدَا ", "بِعْتِئِدْ, حَسَبْ خِبِرْتِي.  "]
    random_choice = random.choice(random_answsers)
    msg = random_choice + most_common_color
    tts(msg, "ar-LB")
    # tts(" ","en-US")
    # return msg  
    
if __name__ == "__main__":
    main()
#"Slate Gray (Dark) !Dark Slate Gray"," رْمَادِيِ  غَامِقْ","#2F4F4F","47","79","79","180","25","25"