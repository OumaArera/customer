from .settings import *

DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME': ':memory:',  # In-memory SQLite for fast tests
		}
	}