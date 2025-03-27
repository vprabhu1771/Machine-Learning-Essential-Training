import tkinter as tk
from tkinter import filedialog, messagebox
import os
import cv2
import pickle
import face_recognition
from imutils import paths


# Function to process dataset and save face encodings
def load_dataset():
    dataset_folder_path = filedialog.askdirectory(title="Select Dataset Folder")

    if not dataset_folder_path:
        messagebox.showwarning("Warning", "No folder selected!")
        return

    print("[INFO] Start processing faces...")
    imagePaths = list(paths.list_images(dataset_folder_path))

    knownEncodings = []
    knownNames = []

    for (i, imagePath) in enumerate(imagePaths):
        print("[INFO] Processing image {}/{}".format(i + 1, len(imagePaths)))
        name = os.path.basename(os.path.dirname(imagePath))  # Extract person's name

        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect face locations
        boxes = face_recognition.face_locations(rgb, model="hog")

        # Encode faces
        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding in encodings:
            knownEncodings.append(encoding)
            knownNames.append(name)

    # Save encodings to a file
    print("[INFO] Serializing encodings...")
    encoding_data = {"encodings": knownEncodings, "names": knownNames}
    with open("encodings.pickle", "wb") as f:
        f.write(pickle.dumps(encoding_data))

    messagebox.showinfo("Success", "Dataset processing complete!\nEncodings saved to 'encodings.pickle'.")


# Function to recognize faces in an image
def recognize_face():
    image_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])

    if not image_path:
        messagebox.showwarning("Warning", "No image selected!")
        return

    # Load the saved encodings
    if not os.path.exists("encodings.pickle"):
        messagebox.showerror("Error", "No dataset found! Please load a dataset first.")
        return

    print("[INFO] Loading encodings...")
    with open("encodings.pickle", "rb") as f:
        data = pickle.load(f)

    # Load the input image and detect faces
    image = cv2.imread(image_path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    boxes = face_recognition.face_locations(rgb, model="hog")
    encodings = face_recognition.face_encodings(rgb, boxes)

    names = []

    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"

        if True in matches:
            matchedIdxs = [i for i, match in enumerate(matches) if match]
            counts = {}

            for idx in matchedIdxs:
                matched_name = data["names"][idx]
                counts[matched_name] = counts.get(matched_name, 0) + 1

            name = max(counts, key=counts.get)

        names.append(name)

    # Draw results on image
    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(image, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show image
    cv2.imshow("Face Recognition", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    messagebox.showinfo("Result", f"Recognized: {', '.join(names)}")


# Create Tkinter window
root = tk.Tk()
root.geometry("400x400")
root.title("Face Recognition")

# Buttons
load_dataset_btn = tk.Button(root, text="Load Dataset", command=load_dataset, font=("Arial", 12), padx=10, pady=5)
load_dataset_btn.pack(pady=20)

recognize_face_btn = tk.Button(root, text="Recognize Face", command=recognize_face, font=("Arial", 12), padx=10, pady=5)
recognize_face_btn.pack(pady=20)

root.mainloop()