```
https://github.com/wasiongit/ANPR_with_opencv/tree/main
```

```python
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2

# Load the Haar cascade for number plate detection
plate_cascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")

def detect_number_plate(file_path):
    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
    for (x, y, w, h) in plates:
        area = w * h
        if area > 500:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "Number Plate", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    return img

def open_file():
    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
    )
    if file_path:
        result_img = detect_number_plate(file_path)

        # Convert OpenCV image (BGR) to PIL image (RGB)
        result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(result_img)
        imgtk = ImageTk.PhotoImage(image=pil_img)

        img_label.config(image=imgtk)
        img_label.image = imgtk
        print("working")

def detect_number_plate(file_path):
    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
    count = 0
    for (x, y, w, h) in plates:
        area = w * h
        if area > 500:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "Number Plate", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)


            # Crop and save
            roi = img[y:y+h, x:x+w]
            save_path = f"plate_{count}.jpg"
            cv2.imwrite(save_path, roi)
            print(f"Saved cropped plate to {save_path}")
            count += 1

    return img

def open_camera():
    cap = cv2.VideoCapture(0)
    count = 0

    while True:
        success, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        plates = plate_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in plates:
            area = w * h
            if area > 500:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
                cv2.putText(img, "Number Plate", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                roi = img[y:y+h, x:x+w]
                cv2.imshow("Plate", roi)

        cv2.imshow("Live Camera", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):  # Save on 's'
            cv2.imwrite(f"live_plate_{count}.jpg", roi)
            print(f"Saved live_plate_{count}.jpg")
            count += 1
        elif key == ord('q'):  # Quit on 'q'
            break

    cap.release()
    cv2.destroyAllWindows()

# --- Tkinter GUI setup ---
root = tk.Tk()
root.title("Number Plate Recognizer")
root.geometry("800x600")

btn = tk.Button(root, text="Open Image", command=open_file, font=("Arial", 14))
btn.pack(pady=10)

img_label = tk.Label(root)
img_label.pack()

btn_cam = tk.Button(root, text="Open Camera", command=open_camera, font=("Arial", 14))
btn_cam.pack(pady=5)


root.mainloop()
```
