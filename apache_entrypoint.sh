#!/bin/sh
python3 manage.py makemigrations
python3 manage.py migrate
yes | python3 manage.py collectstatic

cd ..
echo "export SECRET_KEY=***
export SENDGRID_API_KEY=***
export DATABASE_URL=***
export SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=***
export SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=***
export CLIENT_ID=***
export GOOGLE_CLIENT_SECRET=/home/carbonara.com/backend/client_secret.json
export GOOGLE_APPLICATION_CREDENTIALS=***" > .env
chmod +x .env

a2dissite 000-default
a2ensite carbonara
service apache2 reload
service apache2 restart

cd backend 
python3 manage.py runserver 0.0.0.0:8000
