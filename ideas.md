API server for the main page


Project structure
- Landing Page
	- Admin Dashboard
		- Maps
		- System Architecture
		- Data streaming
	- User Dashboard
		- Account & auth
		- Profile
		- Rides available
	- Drivers Dashboard
		- Account
		- Rides
		- Auth

APIs needed
- Google Python Auth
- Google Maps API
- Email API (for email verification)
- PubNub API (for realtime mapping)
- MoMo API

Database System
- Firebase NoSQL
- PostgreSQL

Database Backup technologies
- Remote postgresql database backup

Data Streaming
- AJAX requests
- WebSockets

Platform functions
- Registering Drivers
- Permission to delete users/drivers from System
- Fixed shuttle rates
- Realtime ride monitoring
- Barcode Generation (BETA function)
- Realtime Map of shuttles
- Usage amount monitoring
- Ride destinations
- Geotagged campus destinations


Database structure
- Users 
	- UID (user ID)
	- Name
	- Level
	- Course
	- Residence
	- Email
	- Account_bal

- Drivers/Shuttle Operators
	- DID (driver ID)
	- Name
	- Profile Picture
	- Mobile Number
	- Routes

- Admin
	- AID (admin ID)
	- Name
	- Profile Picture
	- Email
	- Permissions
		- Ability to add/delete drivers
		- Ability to monitor data (eg. rides, money, usage, etc...)


