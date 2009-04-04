"""
BeamAuth models
"""

from django.db import models
from django.contrib.auth.models import User

from utils import *

class UserSecret(models.Model):
  user = models.ForeignKey(User, primary_key = True)
  secret = models.CharField(max_length=50)
  
  @classmethod
  def generate_for_user(cls, user):
    secret, created_p = cls.objects.get_or_create(user= user)
    if created_p:
      secret.secret = random_string(20)
      secret.save()
    return secret