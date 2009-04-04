"""
URLs for BeamAuth App

ben@adida.net
"""

from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
    (r'^$', index),
    
    (r'^register$', register),
    (r'^wait$', wait),
    (r'^login$', login),
    (r'^confirm$', confirm),
    (r'^resend_secret$', resend_secret),
    (r'^send_password_reset_link$', send_password_reset_link),
    (r'^password_reset$', password_reset),
    (r'^logout$', logout),
)
