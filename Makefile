run:
	cd frontend/; 			\
	npm run build; 			\
	cd ../backend/; 		\
	docker-compose up --build
build:
	cd frontend/; 			\
	npm run build;			\
	cd ../backend;			\
	docker-compose build

superuser:
	cd backend/;			\
	docker exec -it backend_web_1 python manage.py createsuperuser

debug:
	cd backend/;			\
	docker-compose up -d adminer;	\
	docker-compose up -d db;	\
	docker-compose up -d web;	\
	docker exec -it backend_web_1 python debug_manage.py runserver 0.0.0.0:5000 --noreload

shell:
	docker exec -it backend_web_1 /bin/bash
