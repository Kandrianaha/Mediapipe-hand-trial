try:
    import cv2
    import mediapipe as mp
except Exception as e:
    print("Missing required packages:", e)
    print("Install with: pip install opencv-python mediapipe")
    raise

# initialization of mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Access webcam feed
cap = cv2.VideoCapture(0)

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
            for point in hand_landmarks.landmark:
                x, y = int(point.x * frame.shape[1]), int(point.y * frame.shape[0])
                # Draw landmarks 
                cv2.circle(frame, (x, y), 5, (255, 0, 0), -1)

            # Detecting hand gesture here (example rule using thumb landmarks)
            if (hand_landmarks.landmark[4].y > hand_landmarks.landmark[3].y and
                hand_landmarks.landmark[4].y > hand_landmarks.landmark[2].y and
                hand_landmarks.landmark[4].y > hand_landmarks.landmark[1].y and
                hand_landmarks.landmark[4].y > hand_landmarks.landmark[0].y):
                cv2.putText(frame, 'Closed Hand', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame with hand tracking 
    cv2.imshow('Hand Tracking', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Release the video capture and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
