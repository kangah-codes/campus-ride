from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db, login
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From

# Import module models (i.e. User)
from app.module.models import *
import json
import datetime
import sqlalchemy
import string
import random
import requests
import shutil
import os
import uuid

production = True

"""
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 

t0068NQAAALeOt7tCNQDb0VohyHCIeuVhrnEXjppyoyqJg+LX9k3xsxt2l3G5S/p4i1pfWmj5vgKwMxBjFgvFG/X4fXy2FAs= SCANNER


d-f06b610e0a034324bdfa30f17c6738dc 

ADM-000000 campusridegh11

tk_f0f2bb56-6f86-11ea-b8e9-f23c9170642f


"""

if not production:
	url = 'http://127.0.0.1:5000'
else:
	url = 'https://www.campusride.africa'
"""
"""

try:
	nota = Notifications()
	db.session.add(nota)
	db.session.commit()
except:
	db.session.rollback()

try:
	pay = PaymentStats()
	db.session.add(pay)
	db.session.commit()
except Exception as e:
	db.session.rollback()

try:
	payment = Payment()
	db.session.add(payment)
	db.session.commit()

except Exception as e:
	db.session.rollback()


payed = False
cancel = False
pay_amt = 0
invoice = None
error = None




# if Notifications.query.filter_by(date=str(datetime.date.today())).first() is None:
# 	admin_notifications = Notifications()
# else:
# 	admin_notifications = Notifications.query.filter_by(date=str(datetime.date.today())).first()

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('app', __name__)

# global functions
def comparePass(pwd1, pwd2):
	return pwd1 == pwd2

def generateInvoice():
	items = string.ascii_uppercase+string.digits
	return ''.join(random.choice(items) for i in range(6))

def generateAdmin():
	items = string.ascii_uppercase+string.digits
	return 'ADM-'+''.join(random.choice(items) for i in range(6))

def generatePassword():
	items = string.ascii_uppercase+string.digits+string.ascii_lowercase
	return ''.join(random.choice(items) for i in range(8))

# Set the route and accepted methods



# custom route to redirect to login page
@mod_auth.route('/')
def index():
	return render_template('landing_page.html')

# User routes
# login route
@mod_auth.route('/login_user', methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		if current_user.is_admin:
			return redirect('/admin_home')
		return redirect('/home')
	if request.method == "POST":
		stid = request.form.get("id")
		pwd = request.form.get("pwd")
		rem = request.form.get("rem")
		search = User.query.filter_by(public_id=stid).first()
		try:
			if check_password_hash(search.password_hash, pwd):
				if search.is_activated:
					login_user(search, remember=False)
					return redirect('/home')
				else:
					return render_template('user_login.html', error="Activate your account before you attempt a login")
			return render_template('user_login.html', error="Invalid Username/Password")
		except:
			return render_template('user_login.html', error="No account exists for these credentials")
	return render_template('user_login.html')

@mod_auth.route('/login_admin', methods=["GET", "POST"])
def login_admin():
	if current_user.is_authenticated:
		if current_user.is_admin:
			return redirect('/admin_home')
	if request.method == "POST":
		aid = request.form.get('id')
		pwd = request.form.get('pwd')

		search = User.query.filter_by(admin_id=aid).first()

		try:
			if check_password_hash(search.password_hash, pwd):
				login_user(search, remember=True)
				return redirect('/admin_home')
			return render_template('admin_login.html', error="Invalid username/password")
		except:
			return render_template('admin_login.html', error="No account exists for these credentials")
	return render_template('admin_login.html')

@mod_auth.route('/register', methods=["GET", "POST"])
def register():
	global error
	if current_user.is_authenticated:
		return redirect('/home')

	if request.method == "POST":
		error = None
		name = request.form.get('full_name')
		student_id = request.form.get('st_id')
		email = request.form.get('st_mail')
		password = request.form.get('pwd1')
		password_compare = request.form.get('pwd2')
		hall = request.form.get('hall')
		level = request.form.get('level')
		course = request.form.get('course')
		number = request.form.get('phone')

		if not comparePass(password, password_compare):
			error = "Passwords must match"
		else:
			if email.split('@')[-1] == 'st.ug.edu.gh':
				try:
					new_user = User(ids=student_id, email=email, registered_on=datetime.datetime.today(),\
					password_hash=generate_password_hash(password),\
					full_name=name, level=level, momo_number=number)
					new_user.course = course
					new_user.hall = hall
					new_user.is_activated = False
					new_user.is_admin = 0
					new_user.activation_url = str(uuid.uuid1())
					new_user.notifications = json.dumps({f"{datetime.datetime.today()}":f"Account created at {datetime.datetime.today()}"})
					admin_notifications = Notifications.query.filter_by(date=str(datetime.date.today())).first()
					admin_notifications.add_notification(datetime.date.today(), f"User {student_id} created account")
					db.session.add(new_user)
					db.session.add(admin_notifications)
					db.session.commit()
					message = Mail(From('info@ug.campusride.africa', 'Campus Ride'),to_emails=email)
					message.dynamic_template_data = {
					    'link': f'{url}/activate/{new_user.activation_url}'
					}
					message.template_id = 'd-f06b610e0a034324bdfa30f17c6738dc'
					try:
						sendgrid_client = SendGridAPIClient('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')
						response = sendgrid_client.send(message)
					except Exception as e:
						raise Exception("Error")
					login_user(new_user, remember=True)
					return redirect('/')
					return render_template('landing_page.html', success=True)
				except Exception as e:
					print(e)
					db.session.rollback()
					return render_template('user_register.html', error="An account already exists with these credentials")
				finally:
					db.session.close()
			else:
				return render_template('user_register.html', error="You must use your student mail")

	return render_template('user_register.html', error=error)

@mod_auth.route('/activate/<url>')
def activate(url):
	user = User.query.filter_by(activation_url=url).first()
	if user is not None:
		user.activation_url = ""
		user.is_activated = True
		try:
			db.session.add(user)
			db.session.commit()
		except:
			db.session.rollback()
		login_user(user)
		return redirect('/home')
	else:
		return redirect('/')

@mod_auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect('/')

@mod_auth.route('/home')
@login_required
def home():
	data = {
		"first_name":current_user.full_name.split(' ')[0],
		"bal":current_user.account_bal,
		"ride_history":json.loads(current_user.ride_history),
		"payment_history":json.loads(current_user.payment_history),
	}
	return render_template('user_home.html', **data)

@mod_auth.route('/notifications')
@login_required
def notifications():
	data = {
		"ride_history":current_user.ride_history,
		"payment_history":json.loads(current_user.payment_history),
	}
	return render_template('user_notifications.html', **data)

@mod_auth.route('/wallet', methods=["GET", "POST"])
@login_required
def wallet():
	global payed
	global pay_amt
	global cancel
	global invoice
	invoice = generateInvoice()

	data = {
		"bal":current_user.account_bal,
		"payment_url":current_user.payment_url,
		"number":current_user.momo_number,
		"full_name":current_user.full_name,
		"email":current_user.email,
		"invoice": invoice,
		# "pay":payed,
		# "amt":pay_amt,
		# "cancelled":cancel,
		"url":url
	}

	#payed = False
	amt = 0
	cancel = False

	if request.method == "POST":
		payment = request.form.get("amt")
		current_user.temp_payment = int(payment)
		try:
			db.session.add(current_user)
			db.session.commit()
		except:
			db.session.rollback()

	return render_template('user_wallet.html', **data)

@mod_auth.route('/amt', methods=["POST"])
@login_required
def amt():
	current_user.temp_payment = float(request.form['amt'])
	global pay_amt
	pay_amt = current_user.temp_payment

	try:
		db.session.add(current_user)
		db.session.commit()
	except:
		db.session.rollback()
	else:
		db.session.close()

	return ""

@mod_auth.route('/user_pay/<bus>', methods=["POST"])
@login_required
def user_pay(bus):
	global payed
	if current_user.add_ride(bus, datetime.datetime.now()):
		try:
			data = {
				"bal":current_user.account_bal,
				"payment_url":current_user.payment_url,
				"number":current_user.momo_number,
				"full_name":current_user.full_name,
				"email":current_user.email,
				"invoice": invoice,
				"pay":payed,
				# "amt":pay_amt,
				# "cancelled":cancel,
				"url":url
			}
			admin_notifications = Notifications.query.filter_by(date=str(datetime.date.today())).first()
			admin_notifications.add_notification(datetime.date.today(), f"User {current_user.public_id} boarded bus {bus}")
			db.session.add_all([current_user, admin_notifications])
			db.session.commit()
			#payed = True
			return render_template('user_wallet.html', **data)
		except Exception as e:
			db.session.rollback()
	return redirect('/wallet')

@mod_auth.route('/payment_success/<uid>')
@login_required
def success(uid):
	global payed
	if current_user.payment_url == uid:
		global invoice
		current_user.add_cash_in(invoice, datetime.datetime.today(), current_user.temp_payment)
		try:
			data = {
				"bal":current_user.account_bal,
				"payment_url":current_user.payment_url,
				"number":current_user.momo_number,
				"full_name":current_user.full_name,
				"email":current_user.email,
				"invoice": invoice,
				"amt":current_user.temp_payment,
				"url":url
			}
			admin_notifications = Notifications.query.filter_by(date=str(datetime.date.today())).first()
			if PaymentStats.query.filter_by(date=str(datetime.date.today())).first() is None:
				pay = PaymentStats()
			else:
				pay = PaymentStats.query.filter_by(date=str(datetime.date.today())).first()
			payments = Payment.query.filter_by(id=1).first()
			payments.update(current_user.temp_payment)
			pay.add_payment(current_user.temp_payment)
			admin_notifications.add_notification(datetime.date.today(), f"User {current_user.public_id} credited account with {current_user.temp_payment}")
			current_user.temp_payment = 0
			db.session.add_all([current_user, admin_notifications, pay, payments])
			db.session.commit()
		except Exception as e:
			#print(e)
			#payed = False
			data['pay'] = False
			return render_template('user_wallet.html', **data)
			db.session.rollback()
		else:
			db.session.close()
			# payed = True
			data['pay'] = True
			return render_template('user_wallet.html', **data)
		return redirect('/wallet')
	return redirect('/pay')

@mod_auth.route('/payment_cancelled/<uid>')
@login_required
def cancelled(uid):
	if current_user.payment_url == uid:
		data = {
			"bal":current_user.account_bal,
			"payment_url":current_user.payment_url,
			"number":current_user.momo_number,
			"full_name":current_user.full_name,
			"email":current_user.email,
			"invoice": invoice,
			"cancelled":True,
			"url":url
		}
		
		current_user.temp_payment = 0
		db.session.add(current_user)
		db.session.commit()
		return render_template('user_wallet.html', **data)
	return redirect('/')

@mod_auth.route('/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
	error = None
	data = {
		"first_name":current_user.full_name.split(' ')[0],
		"last_name":current_user.full_name.split(' ')[-1],
		"stid":current_user.public_id,
		"email":current_user.email,
		"hall":current_user.hall,
		"number":current_user.momo_number,
		"level":current_user.level,
		"course":current_user.course,
		"full_name":current_user.full_name,
	}

	if request.method == "POST":
		hall = request.form.get("hall")
		number = request.form.get("number")
		level = request.form.get("level")
		course = request.form.get("course")

		current_user.hall = hall
		current_user.momo_number = number
		current_user.level = level
		current_user.course = course

		try:
			db.session.add(current_user)
			db.session.commit()
		except:
			error = "Server error, please try later"
			db.session.rollback()
		
		return redirect('/profile')	

	return render_template('user.html', **data)

@mod_auth.route('/pay')
@login_required
def pay():
	data = {
		"buses": Bus.query.all(),
		"amount": current_user.account_bal
	}
	return render_template('user_payment.html', **data)

@mod_auth.route('/admin_home')
@login_required
def admin_home():
	if current_user.is_admin:
		if PaymentStats.query.filter_by(date=str(datetime.date.today())).first() is None:
			pay = PaymentStats()
		else:
			pay = PaymentStats.query.filter_by(date=str(datetime.date.today())).first()
		today = Notifications.query.filter_by(date=str(datetime.date.today())).first()
		data = {
			"total_day": pay.get_payment(),
			"total": Payment.query.filter_by(id=1).first().amt,
			"today": str(datetime.date.today()),
			"students": db.session.query(User).filter_by(is_admin=False).count(),
			"bus": db.session.query(Bus).count(),
			"students_today": User.query.filter_by(registered_on=str(datetime.date.today()), is_admin=False).all(),
			"notifications":Notifications.query.filter_by(date=str(datetime.date.today()))[:-5:-1],
			"admin":current_user.is_admin,
			"has_permission":current_user.permission == 2
		}
		try:
			data['notif_count'] = len(today.get_notifications())
		except:
			data['notif_count'] = 0
		return render_template('admin_dashboard.html', **data)
	return redirect('/')

@mod_auth.route('/admin_students')
@login_required
def admin_students():
	if current_user.is_admin:
		today = Notifications.query.filter_by(date=str(datetime.date.today())).first()
		data = {
			"students": User.query.filter_by(is_admin=False),
			"notifications":Notifications.query.filter_by(date=str(datetime.date.today()))[:-5:-1],
			"admin":current_user.is_admin,
			"has_permission":current_user.permission == 2

		}
		try:
			data['notif_count'] = len(today.get_notifications())
		except:
			data['notif_count'] = 0
		return render_template('admin_user.html', **data)
	return redirect('/')

@mod_auth.route('/admin_buses')
@login_required
def admin_buses():
	if current_user.is_admin:
		today = Notifications.query.filter_by(date=str(datetime.date.today())).first()
		data = {
			"buses": Bus.query.all(),
			"notifications":Notifications.query.filter_by(date=str(datetime.date.today())),
			"admin":current_user.is_admin,
			"has_permission":current_user.permission == 2
		}
		try:
			data['notif_count'] = len(today.get_notifications())
		except:
			data['notif_count'] = 0
		return render_template('admin_buses.html', **data)
	return redirect('/')

@mod_auth.route('/admin_admin')
@login_required
def admin_admin():
	if current_user.is_admin:
		today = Notifications.query.filter_by(date=str(datetime.date.today())).first()
		data = {
			"admins":User.query.filter_by(is_admin=True).all(),
			"has_permission":current_user.permission == 2
		}
		return render_template('admin_admin.html',**data)
	return redirect('/')

@mod_auth.route('/admin_notifications')
@login_required
def admin_notification():
	if current_user.is_admin:
		today = Notifications.query.filter_by(date=str(datetime.date.today())).first()
		data = {
			"notifications":Notifications.query.filter_by(date=str(datetime.date.today()))[:-5:-1],
			"admin":current_user.is_admin,
			"has_permission":current_user.permission == 2
		}
		try:
			data['notif_count'] = len(today.get_notifications())
		except:
			data['notif_count'] = 0
		return render_template('admin_notifications.html', **data)
	return redirect('/')

@mod_auth.route('/reg_bus', methods=["POST"])
@login_required
def admin_reg_bus():
	if current_user.is_admin:
		plate = request.form.get("plate")
		seats = request.form.get("seats")

		new_bus = Bus()
		new_bus.number_plate = plate
		new_bus.seats = seats
		admin_notifications = Notifications.query.filter_by(date=str(datetime.date.today())).first()
		admin_notifications.add_notification(datetime.date.today(), f"Admin registered bus {plate}")

		db.session.add_all([new_bus, admin_notifications])
		db.session.commit()

		return redirect('/admin_buses')
	return redirect('/')
	#return render_template('qr.html', code=new_bus.qr_id, bus=plate)

@mod_auth.route('/dec_bus/<bus>', methods=["POST"])
@login_required
def dec_bus(bus):
	if current_user.is_admin:
		bus_qr = Bus.query.filter_by(qr_id=bus).first()
		admin_notifications = Notifications.query.filter_by(date=str(datetime.date.today())).first()
		admin_notifications.add_notification(datetime.date.today(), f"Admin decomissioned bus {bus}")
		bus_qr.is_active = False
		db.session.add_all([bus_qr,admin_notifications])
		db.session.commit()
		return redirect('/admin_buses')
	return redirect('/')

@mod_auth.route('/rec_bus/<bus>', methods=["POST"])
@login_required
def rec_bus(bus):
	if current_user.is_admin:
		bus_qr = Bus.query.filter_by(qr_id=bus).first()
		admin_notifications = Notifications.query.filter_by(date=str(datetime.date.today())).first()
		admin_notifications.add_notification(datetime.date.today(), f"Admin recomissioned bus {bus}")
		bus_qr.is_active = True
		db.session.add_all([bus_qr,admin_notifications])
		db.session.commit()
		return redirect('/admin_buses')
	return redirect('/')

@mod_auth.route('/del_user/<ids>', methods=["POST"])
@login_required
def del_user(ids):
	if current_user.is_admin:
		user = User.query.filter_by(public_id=ids).first()
		admin_notifications = Notifications.query.filter_by(date=str(datetime.date.today())).first()
		admin_notifications.add_notification(datetime.date.today(), f"Admin deleted user {user.public_id}")
		db.session.add(admin_notifications)
		db.session.delete(user)
		db.session.commit()
		return redirect('/admin_students')
	return redirect('/')

@mod_auth.route('/reg_admin', methods=["POST"])
@login_required
def add_admin():
	if current_user.is_admin:
		name = request.form.get("name")
		email = request.form.get("email")
		level = request.form.get('level')
		pwd = generatePassword()
		pwd_hash = generate_password_hash(pwd)
		gid = generateAdmin()
		new_admin = User(ids=gid, email=email, registered_on=str(datetime.date.today())\
			, password_hash=pwd_hash, full_name=name, level=0, momo_number=0)
		new_admin.admin_id = gid
		new_admin.is_admin = True
		if level == "Basic":
			new_admin.permission = 1
		else:
			new_admin.permission = 2
		admin_notifications = Notifications.query.filter_by(date=str(datetime.date.today())).first()
		admin_notifications.add_notification(datetime.date.today(), f"Admin registered {name}")
		db.session.add_all([new_admin, admin_notifications])
		db.session.commit()
		message = Mail(
	    from_email='info@campusride.africa',
	    to_emails=email,
	    subject='Account Details',
	    html_content=f"<strong>Username: {gid}<br>Password: {pwd}</strong>")
		try:
			sg = SendGridAPIClient('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')
			response = sg.send(message)
		except Exception as e:
			pass
		#login_user(new_user, remember=True)
		return redirect('/admin_admin')
	return redirect('/')

@mod_auth.route('/bus/<qr>')
@login_required
def bus(qr):
	if current_user.is_admin:
		data = {
			"src":qr
		}
		return render_template("qr.html", **data)
	return redirect('/')