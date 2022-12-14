# spy_agency
spy agency app

run docker-compose up -d --build
then: 
sudo docker exec -ti spy_agency_web_1 bash

Inside of the docker container run:
# migrations
python manage.py migrate spy_agency
python spy_agency/manage.py migrate

# load data
python spy_agency/manage.py loaddata spy_agency

# superuser pass: toor
# all users pass: Password123!
