try:
    import cv2
    import mediapipe as mp
except Exception as e:
    print("Missing required packages:", e)
    print("Install with: pip install opencv-python mediapipe")
    raise

# initialization of mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Access webcam feed
cap = cv2.VideoCapture(0)

# Counting fingers function
def count_fingers(landmarks):
    fingers = 0
    tips = [8, 12, 16, 20]
    for tip in tips:
        if landmarks.landmark[tip].y < landmarks.landmark[tip - 2].y:
                fingers += 1
    return fingers

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to RGB (Mediapipe uses RGB images)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame using Mediapipe Hand Tracking 
    results = hands.process(frame_rgb)

    # If hands are detected, draw landmarks and recognize gestures
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Detecting hand gesture here (example rule using thumb landmarks)
            if (hand_landmarks.landmark[4].y > hand_landmarks.landmark[3].y and
                hand_landmarks.landmark[4].y > hand_landmarks.landmark[2].y and
                hand_landmarks.landmark[4].y > hand_landmarks.landmark[1].y and
                hand_landmarks.landmark[4].y > hand_landmarks.landmark[0].y):
                cv2.putText(frame, 'Closed Hand', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        count = count_fingers(hand_landmarks)
        cv2.putText(frame, f'Fingers: {count}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        if count == 0:
            cv2.putText(frame, 'FLAP!', (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4)


    # Display the frame with hand tracking 
    cv2.imshow('Hand Tracking', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Release the video capture and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
