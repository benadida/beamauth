"""
Utilities

Ben Adida
ben@adida.net
"""

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, loader

from django import http
import django.core.mail as mail

import logging
import sha, base64

import string, random
from xml.dom import minidom

DONE = HttpResponse("done")
ERROR = HttpResponse("error")

def hash_b64(s):
  """
  hash the string using sha1 and produce a base64 output
  removes the trailing "="
  """
  hasher = sha.new(s)
  result= base64.b64encode(hasher.digest())[:-1]
  return result

def hmac_b64(k,s):
  """
  HMAC a value with a key, b64 output no trailing =
  """
  mac = hmac.new(k, s, sha)
  result= base64.b64encode(hasher.digest())[:-1]
  return result

def random_string(length):
    # FIXME: seed!
    return "".join([random.choice(string.letters) for i in range(length)])

def send_mail(subject, body, sender, recipient):
    mail.send_mail(subject, body, sender, recipient)

def redirect(url):
  return HttpResponseRedirect(url)
  
def render_template_raw(template_name, vars, type="html"):
  t = loader.get_template('%s.%s' % (template_name, type))
  c = Context(vars)
  return t.render(c)

def render_template(template_name, vars, type="html"):
  content = render_template_raw(template_name, vars, type)

  mimetype = 'text/plain'

  if type == "html":
    mimetype = "text/html"

  if type == "xml":
    mimetype = "application/xml"

  return HttpResponse(content, mimetype=mimetype)


def get_content_type(request):
    # via straight django or via Apache
    content_type = None
    if request.META.has_key('CONTENT_TYPE'):
        content_type = request.META['CONTENT_TYPE']
    if not content_type and request.META.has_key('HTTP_CONTENT_TYPE'):
        content_type = request.META['HTTP_CONTENT_TYPE']

    return content_type

