import cv2

# Open the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Read a few frames to test the camera
for _ in range(10):
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break
    print("Frame captured")

# Release the webcam
cap.release()

print("Camera test completed successfully.")
