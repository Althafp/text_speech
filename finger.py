import cv2
import mediapipe as mp

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# Initialize MediaPipe drawing module
mp_drawing = mp.solutions.drawing_utils

# Start webcam capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # Flip the image horizontally for a later selfie-view display
    # Convert the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # Process the image and find hands
    results = hands.process(image)

    # Convert the image color back so it can be displayed
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand connections
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Get fingertips (based on MediaPipe hand landmark indices)
            # Thumb tip is landmark 4, index finger tip is landmark 8, etc.
            for id, lm in enumerate(hand_landmarks.landmark):
                # Get the width and height of the image
                h, w, _ = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                # Draw a square box around the fingertip
                if id in [4, 8, 12, 16, 20]:  # Tip landmarks for thumb, index, middle, ring, pinky
                    cv2.rectangle(image, (cx - 10, cy - 10), (cx + 10, cy + 10), (255, 0, 255), -1)

    # Display the resulting frame
    cv2.imshow('Fingertip Detection', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
