from app import db, flask_bcrypt, login
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
import json
import uuid
import string
import random
import datetime

def generate_bus_pin():
	return ''.join(random.choice(string.ascii_uppercase+string.digits) for i in range(6))

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

class RideStats(db.Model):
	__tablename__ = "rides"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	stats = db.Column(db.String(), unique=False, nullable=True)

	def __init__(self):
		self.stats = json.dumps(
			{
				str(datetime.date.today()):0
			}
		)

	def add_amount(self, amount):
		stats = json.loads(self.stats)
		today = str(datetime.date.today())
		for i in stats.keys():
			if today == i:
				stats[i] += amount
			else:
				stats[today] = amount
		self.stats = json.dumps(stats)

	def get_stats(self):
		return json.loads(self.stats).items()

class RegisterStats(db.Model):
	__tablename__ = "register"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	stats = db.Column(db.String(), unique=False, nullable=True)

	def __init__(self):
		self.stats = json.dumps(
			{
				str(datetime.date.today()):0
			}
		)

	def add_register(self, date):
		stats = json.loads(self.stats)
		today = str(datetime.date.today())
		for i in stats.keys():
			if today == i:
				stats[i] += 1
			else:
				stats[today] = 1
		self.stats = json.dumps(stats)

	def get_register(self):
		return json.loads(self.stats).items()


class PaymentStats(db.Model):
	__tablename__ = "payment"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	daily = db.Column(db.String(), unique=False, nullable=True)
	date = db.Column(db.String(), unique=True, nullable=True)

	def __init__(self):
		self.daily = json.dumps({})
		self.date = str(datetime.date.today())

	def add_payment(self, amount):
		daily = json.loads(self.daily)
		today = str(datetime.date.today())

		if today in stats.keys():
			daily[today] += amount

		self.daily = json.dumps(daily)

	def get_payment(self):
		daily = json.loads(self.daily)
		try:
			return daily[str(datetime.date.today())]
		except:
			return 0

	def get_total_payment(self):
		count = json.loads(self.daily)
		sum_all = 0
		for _ in count.values():
			sum_all += _
		return sum_all


class Notifications(db.Model):
	__tablename__ = 'notifications'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	date = db.Column(db.String, unique=True, nullable=True)
	notifications = db.Column(db.String(), unique=False, nullable=True)

	def __init__(self):
		self.notifications = json.dumps([])
		self.date = str(datetime.date.today())

	def add_notification(self, date, text):
		temp = json.loads(self.notifications)
		temp.append(f"{text} at {date}")
		self.notifications = json.dumps(temp)

	def get_notifications(self):
		return json.loads(self.notifications)

	def __repr__(self):
		return f"<Notifications {self.notifications}>"


class Bus(db.Model):
	__tablename__ = "buses"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	qr_id = db.Column(db.String(), unique=True, nullable=True)
	is_active = db.Column(db.Boolean, unique=False, nullable=True)
	alt_id = db.Column(db.Integer, unique=True, nullable=True)
	seats = db.Column(db.Integer, unique=False, nullable=True)
	number_plate = db.Column(db.String(), unique=False, nullable=True)
	registered_on = db.Column(db.String(), unique=False, nullable=True)

	def __init__(self):
		self.qr_id = str(uuid.uuid4())
		self.alt_id = generate_bus_pin()
		self.registered_on = str(datetime.date.today())
		self.is_active = True

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
	email = db.Column(db.String(255), unique=True, nullable=True, default="None")
	registered_on = db.Column(db.String(), nullable=True)
	public_id = db.Column(db.String(100), unique=True)
	hall = db.Column(db.String(), unique=False, nullable=True)
	password_hash = db.Column(db.String(100))
	full_name = db.Column(db.String(100), unique=False, nullable=True)
	level = db.Column(db.String(10), unique=False, nullable=True)
	course = db.Column(db.String(50), unique=False, nullable=True)
	account_bal = db.Column(db.Float(), unique=False, nullable=True, default=1.00)
	momo_number = db.Column(db.String(15), unique=False, nullable=True)
	notifications = db.Column(db.String(), unique=False, nullable=True)
	profile_picture = db.Column(db.String(), unique=False, nullable=True, default="TEST_URL")
	ride_history = db.Column(db.String(), unique=False, nullable=True)
	payment_history = db.Column(db.String(), unique=False, nullable=True)
	activation_url = db.Column(db.String, unique=True, nullable=True)
	is_activated = db.Column(db.Boolean, unique=False, nullable=True, default=False)
	temp_payment = db.Column(db.Float(), unique=False, nullable=True)
	payment_url = db.Column(db.String(), unique=True, nullable=True)
	is_admin = db.Column(db.Boolean, unique=False, nullable=True)
	admin_id = db.Column(db.String(), unique=True, nullable=True)

	def __init__(self, ids, email, registered_on, password_hash, full_name, level, momo_number):
		self.public_id = ids
		self.email = email
		self.registered_on = str(datetime.date.today())
		self.password_hash = password_hash
		self.full_name = full_name
		self.level = level
		self.momo_number = momo_number
		self.ride_history = json.dumps({})
		self.payment_history = json.dumps({})
		self.payment_url = str(uuid.uuid1())

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def add_cash_in(self, txn_id, timestamp, amt):
		try:
			curr_history = json.loads(self.payment_history)
			curr_history[str(timestamp)] = ["credit", str(timestamp), amt]
			self.payment_history = json.dumps(curr_history)
			self.account_bal += amt

		except Exception as e:
			return e

		else:
			return True

	def get_notifications(self):
		return json.loads(self.notifications)

	def add_ride(self, bus_id, timestamp):
		try:
			curr_history = json.loads(self.ride_history)
			curr_history[str(timestamp)] = [bus_id, str(timestamp)]
			self.ride_history = json.dumps(curr_history)
			self.subtract_acc(1)
			payment_history = json.loads(self.payment_history)
			payment_history[str(timestamp)] = ["debit", str(timestamp), 1]
			self.payment_history = json.dumps(payment_history)

		except Exception as e:
			return e

		else:
			return True

	def subtract_acc(self, amt):
		try:
			amount = int(self.account_bal)
			if (amount - amt) >= 0:
				self.account_bal -= amt
				return True
			return False

		except Exception as e:
			return e


	def __repr__(self):
		return "<User '{}'>".format(self.full_name)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
