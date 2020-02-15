# Chatroom backend

Chatroom-backend is a backend server stack for the courtcatch project using Django REST Framework.


## Usage

	cd into root cc-be directory
	$ pip install django
	$ pip install djangorestframework
	$ python3 manage.py runserver
	To authenticate, POST to /auth/ then put the token in the header as such {'Authorization': 'Token <token>'}

## Available Command

	BROWSER	/admin/

