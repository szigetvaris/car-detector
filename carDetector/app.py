from flask import Flask, render_template, request
import requests
import base64
from flask_socketio import SocketIO, emit
import pika
import threading

app = Flask(__name__)


@app.route("/health")
def health():
    return "OK"


@app.route("/upload", methods=["POST"])
def upload():
    if request.method == 'POST':
        tag = request.form.get('tag')
        image = request.files.get('image')

        # send a post request to 0.0.0.0:6000/detect with the image
        payload = {'tag': tag}
        files = {'image': (image.filename, image.read())}
        response = requests.post(
            'http://0.0.0.0:6000/detect', data=payload, files=files)

        # Convert the image data to base64
        image_data = base64.b64encode(response.content).decode('utf-8')

        # Render the image.html template with the image data and title
        return render_template('result.html', title=tag, image_data=image_data)
    else:
        return 'No data received'



# Initalize Flask-SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# RabbitMQ setup
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='car_detector')

def callback(ch, method, properties, body):
    # Wjem a ,essage os receoved, emit it to the WebSocket
    socketio.emit('message', {'data': body.decode()})

# Start consuming messages from RabbitMQ in a new thread
def start_consuming():
    channel.basic_consume(queue='car_detector', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
    
threading.Thread(target=start_consuming).start()

@app.route('/admin')
def admin():
    # Render the admin page
    return render_template('admin.html')

@socketio.on('connect')
def test_connect():
    emit('message', {'data': 'Connected'})

""" 
Main page of the app 
Displays a form where the user can upload an image and tag it with a name
after form is submited the user is redirected to result page where the
image is displayed with the tag name and the recognized cars with bounding
boxes
"""


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)
