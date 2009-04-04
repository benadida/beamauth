"""
BeamAuth views

ben@adida.net
"""

from utils import *
from models import *

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from django.conf import settings

import urllib

def index(request):
  user = request.user
  if user.is_anonymous():
    user = None
  return render_template('index', {'beamauth_root': reverse(index), 'user': user})

def register(request):
  """
  only a post
  """
  if request.POST['password'] != request.POST['password2']:
    return redirect('./')
  
  
  user, create_p = User.objects.get_or_create(email = request.POST['email'], username = hash_b64(request.POST['email']))
  
  # user already existed
  if not create_p:
    return ERROR
    
  # create the user secret
  user.set_password(request.POST['password'])
  user.save()

  generate_secret_and_email(user)
  
  return redirect('./wait')

def resend_secret(request):
  """
  reset the secret for a user
  """
  user = User.objects.get(email = request.GET['email'])
  
  generate_secret_and_email(user)
  
  return redirect('./wait')

def generate_secret_and_email(user):
  """
  generate a (possibly new) secret and email the user the confirmation URL
  """
  secret = UserSecret.generate_for_user(user)
    
  # email the confirmation
  url = settings.WEB_HOST + reverse(confirm) + '?%s#%s' % (urllib.urlencode({'email':user.email}), secret.secret)
  
  send_mail('Beamauth Setup', """

You have successfully registered at Beamauth Bookmark Authentication.
Follow this link to obtain your Beamauth bookmark.

  %s

--
Beamauth Admin""" % url, 'beamauth@adida.net', [user.email])	
    
def send_password_reset_link(request):
  """
  send the link to reset the password
  """
  user = User.objects.get(email = request.GET['email'])
  
  url = settings.WEB_HOST + reverse(password_reset) + '?%s' % urllib.urlencode({'email':user.email, 'verif': user.password})
  
  send_mail('BeamAuth Password Reset', """

You requested a password reset. To pursue this, follow this link:
  
  %s

--
BeamAuth""" % url, 'beamauth@adia.net', [user.email])
  return redirect('./wait')
  
def password_reset(request):
  user = User.objects.get(email = request.REQUEST['email'])
  if user.password == request.REQUEST['verif']:
    if request.method == "GET":
      return render_template('password_reset', {'user': user, 'verif':request.GET['verif']})
    else:
      user.set_password(request.POST['password'])
      user.save()
      return redirect("./")
  else:
    return ERROR

def login(request):
  """
  only a post
  """
  # see if the password is correct
  user_obj = User.objects.get(email = request.POST['email'])
  user = auth.authenticate(username = user_obj.username, password = request.POST['password'])
    
  if not user:
    return ERROR
  
  # see if the secret is correct
  secret = UserSecret.objects.get(user=user)
  if secret.secret == request.POST['secret']:
    auth.login(request, user)
  else:
    return ERROR
    
  return redirect("./")

def confirm(request):
  user = User.objects.get(email = request.GET['email'])
  return render_template('confirm', {'user': user, 'beamauth_root' : reverse(index)})
  
def logout(request):
  auth.logout(request)
  return redirect("./")
  
def wait(request):
  return render_template('wait', {})
