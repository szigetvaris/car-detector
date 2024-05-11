import os
from flask import Flask, render_template, request, send_file
from recognition import car_detector
import pika
import csv

engine = Flask(__name__)


@engine.route("/health")
def health():
    return "OK"


@engine.route("/detect", methods=["POST"])
def detect():
    if request.method == 'POST':
        tag = request.form.get('tag')
        image = request.files.get('image')

        # save the image to a tmp file
        image_path = os.path.join('tmp', image.filename)
        image.save(image_path)

        # Process the image here
        count, image_path = car_detector(image_path)
        
        # append (tag, count) to a file
        with open('db.csv', mode='a') as db:
            writer = csv.writer(db)
            writer.writerow([tag, count])
        
        # send the file content to rabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
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
    engine.run(host="0.0.0.0", port=6000, debug=True)
