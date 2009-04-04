"""
URLs for BeamAuth Server, just send everything to the beamauth app

ben@adida.net
"""

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^beamauth/', include('beamauth.urls')),

    # static hack -- production should bypass this route
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': 'static'}),
)
