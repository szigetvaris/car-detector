""" 
    Car Detector Function
    
    Implements a function which gets one parameter
    @param: image_path: str
    
    Runs a car detection model on the image located at image_path
    Draws bounding boxes around the cars in the image
    Save bounding box image to <original_file_path>_detected.jpg
    count the bounding boxes and return the count as an integer
    and the new file path as a string

"""
import cv2 # opencv-python
import os

# def car_detector(file_path):
#     # get actual path
#     current_path = os.path.dirname(os.path.realpath(__file__))
#     file_path = os.path.join(current_path, file_path)
#     # Load the image
#     image = cv2.imread(file_path)
    
#     # Load the car detector model
#     xml_path = os.path.join(current_path, 'haarcascade_car.xml')
#     car_detector = cv2.CascadeClassifier(xml_path)

#     # Detect cars in the image
#     cars = car_detector.detectMultiScale(image)

#     # Draw bounding boxes around the cars
#     for (x, y, w, h) in cars:
#         cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)

#     # Save the image with the bounding boxes
#     output_path = file_path.split('.')[0] + '_detected.jpg'
#     cv2.imwrite(output_path, image)

#     # Return the number of cars detected and the new file path
#     return len(cars), output_path

#car_detector('tmp/cars.jpg')