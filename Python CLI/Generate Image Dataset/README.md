```
pip install opencv-python
```

```python
import cv2
import os
import argparse

def create_dataset_directory(dataset_path):
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

def open_webcam_and_capture(dataset_path):
    create_dataset_directory(dataset_path)
    cap = cv2.VideoCapture(0)  # Open webcam
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    img_count = len(os.listdir(dataset_path))  # Start counting from existing images
    print("Press SPACE to capture an image. Press 'q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        cv2.imshow("Webcam - Press SPACE to capture, Q to exit", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):  # SPACEBAR to capture image
            img_name = os.path.join(dataset_path, f"image_{img_count:04d}.jpg")
            cv2.imwrite(img_name, frame)
            print(f"Saved: {img_name}")
            img_count += 1
        elif key == ord('q'):  # 'q' to quit
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser(description="Open webcam and save dataset images.")
    parser.add_argument("--dataset", type=str, default="dataset", help="Path to dataset directory")
    args = parser.parse_args()

    open_webcam_and_capture(args.dataset)

if __name__ == "__main__":
    main()
```