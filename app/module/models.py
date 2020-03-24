from app import db, flask_bcrypt, login
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
import json
import uuid
import string
import random

def generate_bus_pin():
	return ''.join(random.choice(string.ascii_uppercase+string.digits) for i in range(6))

class Admin(db.Model):
	__tablename__ = "admin"

	id = db.Column(db.Integer, primary_key=True)
	full_name = db.Column(db.String(255), nullable=False)
	username = db.Column(db.String(20), nullable=False)
	password_hash = db.Column(db.String(20), nullable=False)
	profile_picture = db.Column(db.String(255), nullable=False)

	@property
	def password_hash(self):
		raise AttributeError("View only")

	@password_hash.setter
	def password(self, password):
		self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

	def check_password(self, password):
		return flask_bcrypt.check_password_hash(self.password_hash, password)
	
	def __repr__(self):
		return f"<Admin {self.id}>"

class Driver(db.Model):
	"""
	Driver model for storing driver related details
	"""
	__tablename__ = "drivers"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	full_name = db.Column(db.String(255), nullable=False)
	mobile_number = db.Column(db.String(15), nullable=False)
	profile_picture = db.Column(db.String(255), nullable=False)
	route_history = db.Column(db.String, nullable=True)

	def __repr__(self):
		return f"<Driver {self.id}>"

class Bus(db.Model):
	__tablename__ = "buses"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	qr_id = db.Column(db.String(), unique=True, nullable=False)
	alt_id = db.Column(db.Integer, unique=True, nullable=False)

	def __init__(self):
		self.qr_id = uuid.uuid4()
		self.alt_id = generate_bus_pin()

	def __repr__(self):
		return f"<Bus {self.id}, QR:{self.qr_id}, PIN:{self.alt_id}>"


class Transaction(db.Model):
	__tablename__ = "transactions"

	tx_id = db.Column(db.Integer, primary_key=True)
	sender = db.Column(db.String(100), nullable=True)
	timestamp = db.Column(db.DateTime, nullable=True)
	amount = db.Column(db.String(100), nullable=False)

	def __repr__(self):
		return f"<Transaction {self.tx_id}>"

class User(UserMixin, db.Model):
	""" User Model for storing user related details """
	__tablename__ = "user"

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), unique=True, nullable=False, default="None")
	registered_on = db.Column(db.DateTime, nullable=False)
	public_id = db.Column(db.String(100), unique=True)
	#username = db.Column(db.String(50), unique=True)
	password_hash = db.Column(db.String(100))
	full_name = db.Column(db.String(100), unique=False, nullable=False)
	level = db.Column(db.String(10), unique=False, nullable=False)
	#course = db.Column(db.String(50), unique=False, nullable=False)
	account_bal = db.Column(db.Float(), unique=False, nullable=False, default=1.00)
	momo_number = db.Column(db.String(15), unique=False, nullable=True)
	notifications = db.Column(db.String(), unique=False, nullable=True)
	profile_picture = db.Column(db.String(), unique=False, nullable=True, default="TEST_URL")
	ride_history = db.Column(db.String(), unique=False, nullable=True)
	payment_history = db.Column(db.String(), unique=False, nullable=True)

	def __init__(self, ids, email, registered_on, password_hash, full_name, level, momo_number):
		self.public_id = ids
		self.email = email
		self.registered_on = registered_on
		self.password_hash = password_hash
		self.full_name = full_name
		self.level = level
		self.momo_number = momo_number

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def add_cash_in(self, txn_id, timestamp, amt):
		try:
			curr_history = json.loads(self.payment_history)
			curr_history[txn_id] = [timestamp, amt]
			self.payment_history = json.dumps(curr_history)

		except Exception as e:
			return e

		else:
			return True

	def add_ride(self, bus_id, timestamp):
		try:
			curr_history = json.loads(self.ride_history)
			curr_history[timestamp] = bus_id
			self.ride_history = json.dumps(curr_history)

		except Exception as e:
			return e

		else:
			return True

	def subtract_acc(self, amt):
		try:
			amount = int(self.account_bal)
			if amount - amt >= 0:
				self.account_bal = amount
				return True
			return False

		except Exception as e:
			return e


	def __repr__(self):
		return "<User '{}'>".format(self.full_name)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))