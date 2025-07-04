# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
import sqlalchemy
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.getenv('SECRET_KEY', 'aphrohead')
	DEBUG = False

class DevelopmentConfig(Config):

	BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

	# Define the database - we are working with
	# SQLite for this example
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
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
	SQLALCHEMY_DATABASE_URI = 'postgres://syigawqygvttem:e178f60183852ff7cf3188414ecb6ff6759a5bfd3ac6a9ce1443646a913f5a25@ec2-52-0-155-79.compute-1.amazonaws.com:5432/d88g0vurtncee8'
	PRESERVE_CONTEXT_ON_EXCEPTION = False
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	DATABASE_CONNECT_OPTIONS = {}
	# 60 seconds before a connection is recycled
	SQLALCHEMY_POOL_RECYCLE = 60
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

"""

sqlalchemy.engine.url.URL(
        drivername='postgres+pg8000',
        username=db_user,
        password=db_pass,
        database=db_name,
        query={
            'unix_sock': '/cloudsql/{}/.s.PGSQL.5432'.format(
                cloud_sql_connection_name)
        }
    )

"""
