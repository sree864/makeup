import cv2
import numpy as np
import dlib

# Load the pre-trained face detector and shape predictor
face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Load the lipstick image
lipstick_image = cv2.imread('l1.png')

# Create a mask to remove the white background from the lipstick image
lipstick_mask = cv2.cvtColor(lipstick_image, cv2.COLOR_BGR2GRAY)
_, lipstick_mask = cv2.threshold(lipstick_mask, 1, 255, cv2.THRESH_BINARY)
lipstick_mask = cv2.bitwise_not(lipstick_mask)

# Initialize the video capture object
cap = cv2.VideoCapture(0)

# Perform color quantization on the lipstick image to get dominant colors
Z = lipstick_image.reshape((-1, 3)).astype(np.float32)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 5  # Number of clusters
_, _, centers = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

# Get the dominant red shade from the centers
dominant_red = centers[:, 2].argmax()
dominant_red_color = tuple(map(int, centers[dominant_red]))

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_detector(gray)

    # Iterate over the detected faces
    for face in faces:
        # Predict the facial landmarks
        shape = shape_predictor(gray, face)
        landmarks = np.array([(shape.part(i).x, shape.part(i).y) for i in range(shape.num_parts)], np.int32)

        # Extract the lip region
        lips_region = cv2.convexHull(landmarks[48:61])
        (x, y, w, h) = cv2.boundingRect(lips_region)

        # Resize the lipstick mask to match the lip region size
        lipstick_mask_resized = cv2.resize(lipstick_mask, (w, h))

        # Apply the mask to the lipstick image
        lipstick_roi = cv2.bitwise_and(lipstick_image[y:y + h, x:x + w], lipstick_image[y:y + h, x:x + w], mask=lipstick_mask_resized)

        # Convert the lipstick ROI to HSV color space
        hsv_lipstick_roi = cv2.cvtColor(lipstick_roi, cv2.COLOR_BGR2HSV)

        # Create a mask for the red shades
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 100, 100])
        upper_red2 = np.array([180, 255, 255])
        mask1 = cv2.inRange(hsv_lipstick_roi, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv_lipstick_roi, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)

        # Count the number of pixels in the red shades
        pixel_count = np.sum(mask > 0)

        # If there are red pixels, calculate the average color
        if pixel_count > 0:
            average_color = cv2.mean(lipstick_roi, mask=mask)[:3]
            average_color = tuple(map(int, average_color))
        else:
            # Use the dominant red shade if no red pixels are found
            average_color = dominant_red_color

        # Apply the extracted average color to the lips region
        cv2.fillPoly(frame, [lips_region], average_color)

        # Draw a rectangle around the face
        (x, y, w, h) = (face.left(), face.top(), face.width(), face.height())
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Lipstick Try-On', frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the windows
cap.release()
cv2.destroyAllWindows()
