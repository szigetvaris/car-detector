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

# Port megnyitása
EXPOSE 5000

# Migrációk futtatása
#RUN python manage.py migrate

# Django alkalmazás indítása, a 5000-es porton<
CMD ["python", "manage.py", "runserver", "5000:5000"]
