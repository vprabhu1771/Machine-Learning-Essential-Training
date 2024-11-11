### 4. Basic Drawing Functions
OpenCV allows you to draw shapes like lines, rectangles, and circles on images.

#### Drawing a Line
```python
cv2.line(image, (start_x, start_y), (end_x, end_y), (color_b, color_g, color_r), thickness)
```

Here is a complete program that uses the `cv2.line()` function in OpenCV to draw a line on an image. The program creates a blank image, draws a line from a starting point to an ending point, and displays the result.

```python
import cv2
import numpy as np

# Define image dimensions
image_width = 400
image_height = 400

# Create a blank white image
image = np.ones((image_height, image_width, 3), dtype=np.uint8) * 255

# Define line parameters
start_x, start_y = 50, 50  # Starting coordinates
end_x, end_y = 300, 300    # Ending coordinates
color_b, color_g, color_r = 0, 0, 255  # Color in BGR (red)
thickness = 2  # Line thickness

# Draw the line on the image
cv2.line(image, (start_x, start_y), (end_x, end_y), (color_b, color_g, color_r), thickness)

# Display the image with the line
cv2.imshow("Line Drawing", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Explanation
- **Image creation**: Creates a blank 400x400 white image.
- **Line parameters**:
  - `start_x, start_y` and `end_x, end_y` define the start and end points of the line.
  - `color_b, color_g, color_r` defines the color of the line in BGR format (here, red).
  - `thickness` defines the thickness of the line.
- **`cv2.line`**: Draws the line on the image.
- **Display**: Opens a window displaying the image with the drawn line.

You should have OpenCV (`cv2`) installed to run this program. You can install it with:

#### Drawing a Rectangle
```python
cv2.rectangle(image, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (color_b, color_g, color_r), thickness)
```

Here’s a complete program using the `cv2.rectangle()` function in OpenCV to draw a rectangle on an image. The program creates a blank image, draws a rectangle defined by its top-left and bottom-right corners, and displays the result.

```python
import cv2
import numpy as np

# Define image dimensions
image_width = 400
image_height = 400

# Create a blank white image
image = np.ones((image_height, image_width, 3), dtype=np.uint8) * 255

# Define rectangle parameters
top_left_x, top_left_y = 50, 50           # Top-left corner
bottom_right_x, bottom_right_y = 300, 300  # Bottom-right corner
color_b, color_g, color_r = 0, 255, 0      # Color in BGR (green)
thickness = 3                              # Rectangle border thickness

# Draw the rectangle on the image
cv2.rectangle(image, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (color_b, color_g, color_r), thickness)

# Display the image with the rectangle
cv2.imshow("Rectangle Drawing", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Explanation
- **Image creation**: Creates a blank 400x400 white image.
- **Rectangle parameters**:
  - `top_left_x, top_left_y` defines the top-left corner of the rectangle.
  - `bottom_right_x, bottom_right_y` defines the bottom-right corner.
  - `color_b, color_g, color_r` sets the color in BGR format (here, green).
  - `thickness` defines the thickness of the rectangle's border.
- **`cv2.rectangle`**: Draws the rectangle on the image.
- **Display**: Opens a window showing the image with the rectangle.


#### Drawing a Circle
```python
cv2.circle(image, (center_x, center_y), radius, (color_b, color_g, color_r), thickness)
```


Here's a complete program using the `cv2.circle()` function in OpenCV to draw a circle on an image. The program creates a blank image, draws a circle defined by its center and radius, and displays the result.

```python
import cv2
import numpy as np

# Define image dimensions
image_width = 400
image_height = 400

# Create a blank white image
image = np.ones((image_height, image_width, 3), dtype=np.uint8) * 255

# Define circle parameters
center_x, center_y = 200, 200       # Center of the circle
radius = 100                        # Radius of the circle
color_b, color_g, color_r = 255, 0, 0  # Color in BGR (blue)
thickness = 3                       # Circle border thickness (-1 for filled circle)

# Draw the circle on the image
cv2.circle(image, (center_x, center_y), radius, (color_b, color_g, color_r), thickness)

# Display the image with the circle
cv2.imshow("Circle Drawing", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Explanation
- **Image creation**: Creates a blank 400x400 white image.
- **Circle parameters**:
  - `center_x, center_y` sets the center of the circle.
  - `radius` sets the radius of the circle.
  - `color_b, color_g, color_r` specifies the color in BGR format (here, blue).
  - `thickness` sets the thickness of the circle's border. Use `-1` for a filled circle.
- **`cv2.circle`**: Draws the circle on the image.
- **Display**: Opens a window displaying the image with the circle.

To run this code, you need OpenCV installed: