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
	POST	/users/	body=['username','password','email','first_name','last_name']
	GET	/users/
	GET	/users/<username>
	POST	/users/<username>/change_password	body=['password']
	POST	/boards/	body=['name']
	GET	/boards/
	GET	/boards/<name>
	POST	/boards/<name>/post	body=['message']
