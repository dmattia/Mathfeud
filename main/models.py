from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class GroupProfile(models.Model)
	group = models.ForeignKey(Group, unique=True)
	school = models.CharField(max_length=50)

class UserProfile(models.Model)
	user = models.ForeignKey(User, unique=True)
	group = models.ForeignKey(GroupProfile, unique=True)
