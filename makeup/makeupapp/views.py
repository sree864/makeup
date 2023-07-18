from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector
from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed
import cv2
import numpy as np
import dlib
import base64

import base64

face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor('makeup/makeupapp/shape_predictor_68_face_landmarks.dat')
lipstick_image = cv2.imread('makeup/makeupapp/l1.png')

# Load the lipstick image

# Create a mask to remove the white background from the lipstick image
lipstick_mask = cv2.cvtColor(lipstick_image, cv2.COLOR_BGR2GRAY)
_, lipstick_mask = cv2.threshold(lipstick_mask, 1, 255, cv2.THRESH_BINARY)
lipstick_mask = cv2.bitwise_not(lipstick_mask)

def try_on(request):
    if request.method == 'POST':
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
                    # Use BGR(0, 0, 128) if no red pixels are found
                    average_color = (0, 0, 128)

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

        return render(request, 'sproduct.html')

    else:
        return HttpResponseNotAllowed(['POST'])







#signup page variables
fn=''
ln=''
em=''
pwd=''

def signupaction(request):
    global nm,em,pwd,bday
    if request.method=="POST":
        m = mysql.connector.connect(host="localhost", user="root", passwd="pepperoni@pizzA1", database="makeup")
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items(): 
            if key=="fname":
                fn=value
            if key=="lname":
                ln=value 
            if key=="email":
                em=value
            if key=="password":
                pwd=value           
        c = "INSERT INTO users (firstname, lastname, emailid, password) VALUES ('{}', '{}', '{}', '{}')".format(fn, ln, em, pwd)
        cursor.execute(c)
        m.commit()


    return render(request,'signup_page.html')  

def loginaction(request):
    global em,pwd
    if request.method=="POST":
        m = mysql.connector.connect(host="localhost", user="root", passwd="pepperoni@pizzA1", database="makeup")
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items(): 
            if key=="email":
                em=value
            if key=="password":
                pwd=value           
        c = "SELECT * from users where emailid='{}' and password='{}'".format(em, pwd)
        cursor.execute(c)
        t=tuple(cursor.fetchall())
        if t==():
            return render(request,'error.html')
        else:
            return render(request,'index.html')
    return render(request,'login_page.html')  

def add_to_cart(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        
        # Implement your logic to add the product to the cart
        # Store the product information in the cart database or session
        
        return redirect('cart')  # Redirect to the cart page after adding the product

    return HttpResponseNotAllowed(['POST'])

def cart(request):
    # Retrieve cart items from the database or session
    cart_items = [
        {'product_name': 'Mac Lipstick shade Red Gloss', 'price': 11.8, 'quantity': 1, 'subtotal': 11.8},
        # Add more cart items here
    ]
    
    context = {'cart_items': cart_items}
    return render(request, 'cart.html', context)


def ok(request):
    return render(request,'shop.html')
def ok1(request):
    return render(request,'index.html')    
def ok2(request, product_id):
    # Retrieve the product information based on the product_id from your database
    # You can use the product_id to query the database and get the corresponding name and price

    lipstick_name = "Lipstick Name"  # Replace with the retrieved product name
    lipstick_price = 800  # Replace with the retrieved product price

    context = {
        'lipstick_name': lipstick_name,
        'lipstick_price': lipstick_price,
    }

    return render(request, 'sproduct.html', context)

def ok3(request):
    return render(request,'cart.html')  
def ok4(request):
    return render(request,'login_page.html') 
def ok5(request):
    return render(request,'signup_page.html') 
def ok6(request):
    return render(request,'about.html') 
def ok7(request):
    return render(request,'contact.html') 
def ok8(request):
    return render(request,'sproduct.html') 





