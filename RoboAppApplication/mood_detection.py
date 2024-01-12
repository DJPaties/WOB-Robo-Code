import mediapipe as mp
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

# Mock dataset (replace with your actual dataset)
num_landmarks = 468
X = np.random.rand(100, num_landmarks * 3)  # 3 coordinates (x, y, z) for each landmark
y = np.random.choice(["happy", "sad", "neutral"], size=100)

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train the model
model = make_pipeline(StandardScaler(), SVC())
model.fit(X_train, y_train)

# Initiate holistic model
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture(1)

current_mood = "neutral"
previous_landmarks = None


with mp_holistic.Holistic(
    min_detection_confidence=0.5, min_tracking_confidence=0.5
) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()

        # Recolor Feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Make Detections
        results = holistic.process(image)

        # Check if face landmarks are detected
        if results.face_landmarks is not None:
            facial_landmarks = results.face_landmarks.landmark
            landmarks_array = np.array(
                [[landmark.x, landmark.y, landmark.z] for landmark in facial_landmarks]
            ).flatten()

            # Check if new face is detected, refresh mood prediction
            if previous_landmarks is None or not np.array_equal(
                landmarks_array, previous_landmarks
            ):
                current_mood = model.predict([landmarks_array])[0]
                previous_landmarks = landmarks_array

            # Draw recolored face landmarks with reduced radius
            for landmark in facial_landmarks:
                x, y = int(landmark.x * frame.shape[1]), int(
                    landmark.y * frame.shape[0]
                )
                if current_mood == "happy":
                    color = (0, 255, 0)  # Green
                elif current_mood == "sad":
                    color = (0, 0, 255)  # Red
                else:
                    color = (255, 255, 255)  # White
                cv2.circle(image, (x, y), 2, color, -1)

            # Display the current mood on the frame
            cv2.putText(
                image,
                f"Mood: {current_mood}",
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

            cv2.imshow("Mood Detection", image)

            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

cap.release()
cv2.destroyAllWindows()
