import cv2
import numpy as np
import dlib

# Load the pre-trained face detector and shape predictor
face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Load the lipstick image
lipstick_image = cv2.imread('l1.png')
lipstick_mask = cv2.cvtColor(lipstick_image, cv2.COLOR_BGR2GRAY)
_, lipstick_mask = cv2.threshold(lipstick_mask, 1, 255, cv2.THRESH_BINARY)
lipstick_mask = cv2.bitwise_not(lipstick_mask)

# Initialize the video capture object
cap = cv2.VideoCapture(0)

# Perform color quantization on the lipstick image to get dominant colors
Z = lipstick_image.reshape((-1, 3)).astype(np.float32)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 5  # Number of clusters
_, labels, centers = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_detector(gray)

    for face in faces:
        shape = shape_predictor(gray, face)
        landmarks = np.array([(shape.part(i).x, shape.part(i).y) for i in range(shape.num_parts)], np.int32)

        lips_region = cv2.convexHull(landmarks[48:61])
        (x, y, w, h) = cv2.boundingRect(lips_region)

        lipstick_mask_resized = cv2.resize(lipstick_mask, (w, h))

        # Find the cluster index that corresponds to a shade of red with low G and B values
        red_cluster = None
        for i, center in enumerate(centers):
            b, g, r = center
            if r > 110 and g < 70 and b < 70:  # Adjust these thresholds as needed
                red_cluster = i
                break

        if red_cluster is not None:
            # Apply the color from the red_cluster to the lips region (in BGR format)
            color = [int(val) for val in centers[red_cluster]]  # Reverse the order to BGR
            cv2.fillPoly(frame, [lips_region], color)

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
