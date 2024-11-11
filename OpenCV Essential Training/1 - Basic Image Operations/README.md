### 2. Basic Image Operations
OpenCV provides functions to load, display, and save images.

#### Loading and Displaying an Image
```python
import cv2

# Load an image
image = cv2.imread("path/to/image.jpg")

# Display the image in a window
cv2.imshow("Image", image)

# Wait for a key press and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### 3. Grayscale Conversion
Convert an image to grayscale:

```python
import cv2

# Load an image
image = cv2.imread("path/to/image.jpg")

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Display the image in a window
cv2.imshow("Image", image)

# Wait for a key press and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
```


#### Saving an Image
```python
import cv2

# Load an image
image = cv2.imread("path/to/image.jpg")

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Display the image in a window
cv2.imshow("Image", image)

cv2.imwrite("path/to/save_image.jpg", image)

# Wait for a key press and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
```