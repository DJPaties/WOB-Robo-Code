import numpy as np
import cv2
from PIL import Image
from collections import Counter

def color_range(color):
    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    # Define lower and upper HSV limits with a tolerance of ±10 in the hue component.
    lolim = hsvC[0][0][0] - 10, 100, 100
    uplim = hsvC[0][0][0] + 10, 255, 255

    lolim = np.array(lolim, dtype=np.uint8)
    uplim = np.array(uplim, dtype=np.uint8)
    return lolim, uplim

def get_dominant_color(frame):
    # Convert the frame to the HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the region of interest (ROI) in the center of the frame
    height, width, _ = frame.shape
    roi_width, roi_height = int(0.5 * width), int(0.5 * height)
    roi_x = int(0.25 * width)
    roi_y = int(0.25 * height)
    roi = hsv_frame[roi_y : roi_y + roi_height, roi_x : roi_x + roi_width]

    # Flatten the ROI and calculate the mean color values
    flat_roi = roi.reshape((-1, 3))
    mean_color = np.median(flat_roi, axis=0)

    # Convert the mean color values to integer
    mean_color = mean_color.astype(np.uint8)

    return mean_color

colors = {
    "yellow": [0, 255, 255],  # BGR format
    "blue": [120, 50, 50],  # BGR format
    "red": [0, 0, 255],  # BGR format
    "green": [60, 255, 60],  # BGR format
    
}

cap = cv2.VideoCapture(0)

color_frequencies = Counter()
frame_counter = 0
frames_to_read = 50

while True:
    ret, frame = cap.read()

    # Get the dominant color in the center of the frame
    dominant_color = get_dominant_color(frame)

    # Find the closest color in your predefined color list
    closest_color = min(
        colors, key=lambda x: np.linalg.norm(np.array(colors[x]) - dominant_color)
    )

    # Update color frequency
    color_frequencies[closest_color] += 1

    # Draw a circle instead of a rectangle with the detected color
    center_x, center_y = frame.shape[1] // 2, frame.shape[0] // 2
    radius = 50  # Adjust the radius as needed
    frame = cv2.circle(frame, (center_x, center_y), radius, colors[closest_color], 5)

    # Draw an indicator for the center
    frame = cv2.circle(frame, (center_x, center_y), 5, (255, 255, 255), -1)

    print(
        f"Detected {closest_color} at center. Center coordinates: ({center_x}, {center_y})"
    )

    # Display the frame with color recognition
    cv2.imshow("Color Recognition", frame)

    frame_counter += 1

    # Break the loop after reading the specified number of frames
    if frame_counter >= frames_to_read:
        break

# Display color frequencies
print("Color Frequencies:")
for color, frequency in color_frequencies.items():
    print(f"{color}: {frequency}")

# Find and print the highest frequency color
highest_frequency_color = color_frequencies.most_common(1)[0][0]
print(f"\nHighest Frequency Color: {highest_frequency_color} ({color_frequencies[highest_frequency_color]} times)")

cap.release()
cv2.destroyAllWindows()