FROM ubuntu

# Python
RUN apt-get update
RUN apt-get install -y python3 python3-pip libmysqlclient-dev
ENV PYTHONBUFFERED 1
RUN mkdir /home/carbonara.com
ADD . /home/carbonara.com
WORKDIR /home/carbonara.com/backend
RUN pip3 install -r requirements.txt

# Apache
RUN apt-get install -y apache2 libapache2-mod-wsgi-py3
RUN echo ". /home/carbonara.com/.env" >> /etc/apache2/envvars