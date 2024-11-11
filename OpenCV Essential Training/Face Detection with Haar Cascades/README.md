
```python
import cv2

# Load the cascade for face detection (use the OpenCV provided path)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Load an image from file
image = cv2.imread("OfficialPortrait-2.jpg")

# Check if the image is loaded properly
if image is None:
    print("Error: Could not load image.")
    exit()

# Convert image to grayscale for better accuracy in face detection
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Check if any faces are detected
if len(faces) == 0:
    print("No faces detected.")
else:
    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Display the output image with faces highlighted
    cv2.imshow("Detected Faces", image)
    cv2.waitKey(0)

cv2.destroyAllWindows()
```

To capture video from a webcam and perform face detection in real-time, you can use OpenCV's `cv2.VideoCapture` function. Here’s a code snippet that captures video, detects faces in each frame, and displays the result:

```python
import cv2

# Load the cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Initialize the webcam (0 is the default webcam)
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # If the frame was not captured correctly, break from the loop
    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Display the frame with the faces highlighted
    cv2.imshow("Video - Face Detection", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
```

### Explanation
1. **Initialize Video Capture**: `cv2.VideoCapture(0)` opens the default webcam.
2. **Loop Through Each Frame**: Reads frames continuously from the webcam until 'q' is pressed.
3. **Convert Frame to Grayscale**: Improves face detection accuracy.
4. **Detect Faces**: Finds faces in each frame.
5. **Draw Rectangles**: Highlights faces with rectangles.
6. **Display Frame**: Displays each frame with detected faces in real-time.
7. **Quit Key**: The loop exits if 'q' is pressed.

### Notes
- Ensure your webcam is accessible and drivers are installed.
- Press 'q' to stop the video capture and close the window.