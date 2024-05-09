import os
from flask import Flask, render_template, request, send_file
from recognition import car_detector

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

        return send_file(image_path, mimetype='image/jpeg')
    else:
        return 'No data received'


@engine.route("/")
def home():
    return "hello, this is the car detector engine"


if __name__ == '__main__':
    engine.run(host="0.0.0.0", port=6000, debug=True)
