### 8. Video Capture
You can use OpenCV to capture and process video from a webcam.

```python
import cv2

# Capture video from webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally (1 means horizontal flip)
    frame = cv2.flip(frame, 1)

    # Display the frame
    cv2.imshow("Video", frame)
    
    # Break on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### 9. Reading and Displaying Frames from a Video File
```python
import cv2

cap = cv2.VideoCapture("path/to/video.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```