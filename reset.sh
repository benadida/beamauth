#!/bin/bash
dropdb beamauth
createdb beamauth
python manage.py syncdb