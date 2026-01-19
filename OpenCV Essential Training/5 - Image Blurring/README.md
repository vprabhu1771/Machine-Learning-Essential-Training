### 6. Image Blurring
Blurring helps reduce noise in an image.

#### Gaussian Blur
```python
blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
```

```python
import cv2

# Load an image
image = cv2.imread("jack.png")

blurred_image = cv2.GaussianBlur(image, (25, 25), 0)

# Display the image in a window
cv2.imshow("Image", blurred_image)

# Wait for a key press and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
```
