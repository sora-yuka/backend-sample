r:
	./manage.py runserver 0.0.0.0:8000

m:
	./manage.py makemigrations
	./manage.py migrate

up:
	./manage.py loaddata utilities/fixtures/account_data.json

test-account:
	./manage.py test applications.account.tests