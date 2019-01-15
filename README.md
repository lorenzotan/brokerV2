# Broker App V2
improved version of streamline-broker

# Setup Instructions

#### Download Repo
1. $ git clone https://github.com/lorenzotan/brokerV2.git


#### Create Database
2. $ cd brokerV2/broker/
3. $ python manage.py makemigrations accounts loans
4. $ python manage.py migrate


#### Preload Tables with (qualifiers, property types, loan types, needs list) data
5. $ python manage.py loaddata loans/fixtures/init_*


#### Create super user (you will be prompted for a username, email, password)
6. $ python manage.py createsuperuser


#### Run App
7. $ python manage.py runserver


#### from here, you can log into the admin page with your super user account
8. http://127.0.0.1:8000/admin/
