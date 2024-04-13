# Alap Docker image
FROM python:3.6.15-slim-buster

# Követelmények telepítése
RUN pip3 install django

# Felhasználó létrehozása
RUN useradd pythonuser -ms /bin/bash

# Munkakönyvtár létrehozása és beállítása
WORKDIR /home/pythonuser/app

# Felhasználó beállítása
USER pythonuser

# Projekt másolása a konténerbe
COPY . /home/pythonuser/app/

# Collect static files
#RUN python manage.py collectstatic --noinput

# Django alkalmazás indítása
CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]
