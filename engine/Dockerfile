FROM python:3.7
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx
RUN pip3 install flask flask_socketio pika opencv-python
RUN useradd pythonuser -ms /bin/bash
RUN mkdir -p /home/pythonuser/app/tmp && chown -R pythonuser:pythonuser /home/pythonuser/app/tmp
WORKDIR /home/pythonuser/app
USER pythonuser
COPY engine.py engine.py
COPY haarcascade_car.xml haarcascade_car.xml
CMD python -u engine.py