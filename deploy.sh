#! /bin/bash

# echo '[*] Running tests'
# cd backend && python manage.py test

ssh carbonara@*** "
cd ~/Carbonara
git pull

# Frontend
cd ~/Carbonara/frontend
npm run build

# Backend
cd ~/Carbonara/backend
source env/bin/activate
source .env
python manage.py makemigrations
python manage.py migrate
echo 'yes' | python manage.py collectstatic
touch ~/Carbonara/backend/carbonara/wsgi.py
"
