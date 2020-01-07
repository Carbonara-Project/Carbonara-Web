FROM python:3
ENV PYTHONBUFFERED 1
RUN mkdir /home/carbonara
WORKDIR /home/carbonara
ADD . .
RUN pip install -r requirements.txt

# CMD gunicorn --bind 0.0.0.0:$PORT carbonara.wsgi
CMD python manage.py makemigrations
CMD python manage.py migrate
# CMD python manage.py runserver 0.0.0.0:$PORT
