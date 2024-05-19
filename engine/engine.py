import os
from flask import Flask, render_template, request, send_file
import pika
import csv
import cv2

engine = Flask(__name__)


@engine.route("/health")
def health():
    return "OK"

def car_detector(file_path):
    # get actual path
    current_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_path, file_path)
    # Load the image
    image = cv2.imread(file_path)
    
    # Load the car detector model
    xml_path = os.path.join(current_path, 'haarcascade_car.xml')
    car_detector = cv2.CascadeClassifier(xml_path)

    # Detect cars in the image
    cars = car_detector.detectMultiScale(image)

    # Draw bounding boxes around the cars
    for (x, y, w, h) in cars:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # Save the image with the bounding boxes
    output_path = file_path.split('.')[0] + '_detected.jpg'
    cv2.imwrite(output_path, image)

    # Return the number of cars detected and the new file path
    return len(cars), output_path


@engine.route("/detect", methods=["POST"])
def detect():
    if request.method == 'POST':
        tag = request.form.get('tag')
        image = request.files.get('image')

        # create tmp folder if needed
        # os.makedirs('tmp', exist_ok=True)
        # save the image to a tmp file
        image_path = os.path.join('tmp', image.filename)
        image.save(image_path)
        
        # image.save(image.filename)

        # Process the image here
        count, image_path = car_detector(image_path)
        
        # append (tag, count) to a file
        with open('db.csv', mode='a') as db:
            writer = csv.writer(db)
            writer.writerow([tag, count])
        
        # send the file content to rabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('0.0.0.0'))
        channel = connection.channel()
        channel.queue_declare(queue='car_detector')
        
        with open('db.csv', mode='r', newline="") as db:
            file_content = db.read()
            
        channel.basic_publish(exchange='', routing_key='car_detector', body=file_content)
        connection.close()

        return send_file(image_path, mimetype='image/jpeg')
    else:
        return 'No data received'


@engine.route("/")
def home():
    return "hello, this is the car detector engine"


if __name__ == '__main__':
    engine.run(host="0.0.0.0", port=6000, debug=False)
