BeamAuth
ben@adida.net
http://ben.adida.net/projects/beamauth


BeamAuth uses a bookmark as a second authentication factor to complement a password.
This is prototype/proof-of-concept software, it's not meant for immediate production deployment.

INSTALLATION:
- Python 2.5+
- Django 1.0+
- PostgreSQL 8.2+ (though this may work with MySQL)

- modify settings.py, specifically: DATABASE_NAME and other database parameters potentially
- modify WEB_HOST to the URL where you're running the server
- the EMAIL_* parameters for email

- you can use email_debugger.py if you want to just see what emails would get sent, at the prompt:
python email_debugger.py

