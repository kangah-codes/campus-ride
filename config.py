# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.getenv('SECRET_KEY', 'aphrohead')
	DEBUG = False

class DevelopmentConfig(Config):

	BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

	# Define the database - we are working with
	# SQLite for this example
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
	#SQLALCHEMY_DATABASE_URI = 'postgres://hvqhidstfdeetm:9ca3a9492da4d277312046186f7cc8c969602fa377ff107d8b60048beb9eedde@ec2-34-202-7-83.compute-1.amazonaws.com:5432/d5khtdmlbch2t0'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	DATABASE_CONNECT_OPTIONS = {}

	# Application threads. A common general assumption is
	# using 2 per available processor cores - to handle
	# incoming requests using one and performing background
	# operations using the other.
	THREADS_PER_PAGE = 2

	# Enable protection agains *Cross-site Request Forgery (CSRF)*
	CSRF_ENABLED     = True

	# Use a secure, unique and absolutely secret key for
	# signing the data. 
	CSRF_SESSION_KEY = "secret"

	# Secret key for signing cookies
	SECRET_KEY = "secret"
	DEBUG = True


class TestingConfig(Config):
	DEBUG = True
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'postgres://hvqhidstfdeetm:9ca3a9492da4d277312046186f7cc8c969602fa377ff107d8b60048beb9eedde@ec2-34-202-7-83.compute-1.amazonaws.com:5432/d5khtdmlbch2t0'
	PRESERVE_CONTEXT_ON_EXCEPTION = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
	DEBUG = False
	TESTING = False
	SQLALCHEMY_DATABASE_URI = 'postgres://tdcllfsruioqbz:1f4779fba92ae0091b89353a3b74167af2732839d7cc5da0552e54032023cdea@ec2-52-207-25-133.compute-1.amazonaws.com:5432/d6nemaka83c6sq'
	PRESERVE_CONTEXT_ON_EXCEPTION = False
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	DATABASE_CONNECT_OPTIONS = {}

	# Application threads. A common general assumption is
	# using 2 per available processor cores - to handle
	# incoming requests using one and performing background
	# operations using the other.
	THREADS_PER_PAGE = 2

	# Enable protection agains *Cross-site Request Forgery (CSRF)*
	CSRF_ENABLED     = True

	# Use a secure, unique and absolutely secret key for
	# signing the data. 
	CSRF_SESSION_KEY = "secret"

	# Secret key for signing cookies
	SECRET_KEY = "secret"

config_by_name = dict(
    dev=ProductionConfig,
    )
