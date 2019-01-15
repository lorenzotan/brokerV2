# brokerV2
improved version of streamline-broker

# setup instructions
# download repo
$ git clone https://github.com/lorenzotan/brokerV2.git


# create database
$ cd brokerV2/broker/
$ python manage.py makemigrations accounts loans
$ python manage.py migrate


# preload tables with (qualifiers, property types, loan types, needs list) data
$ python manage.py loaddata loans/fixtures/init_*


# create super user
# you will be prompted for a username, email, password
$ python manage.py createsuperuser


# run webapp
$ python manage.py runserver


# from here, you can log into the admin page with your super user account
# http://127.0.0.1:8000/admin/
