FROM python:3.6.15-slim-buster
RUN pip3 install flask flask_socketio pika
RUN useradd pythonuser -ms /bin/bash
WORKDIR /home/pythonuser/app
USER pythonuser
COPY engine.py engine.py
CMD python -u engine.py