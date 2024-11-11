### 5. Image Resizing
```python
import cv2

# Load an image
image = cv2.imread("path/to/image.jpg")

new_width = 400

new_height = 400

resized_image = cv2.resize(image, (new_width, new_height))

# Display the image in a window
cv2.imshow("Image", resized_image)

# Wait for a key press and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
```