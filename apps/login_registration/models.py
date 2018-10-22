from __future__ import unicode_literals
from django.db import models
import re
import datetime
import calendar

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors['first_name'] = "You must provide a first name"
        elif len(postData['first_name']) < 2:
            errors['first_name'] = "First name must have at least 2 letters"
        elif not postData['first_name'].isalpha():
            errors['first_name'] = "First name can only contain letters"

        if len(postData['last_name']) < 1:
            errors['last_name'] = "You must provide a last name"
        elif len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must have at least 2 letters"
        elif not postData['last_name'].isalpha():
            errors['last_name'] = "Last name can only contain letters"

        if len(postData['email']) < 1:
            errors['email'] = "You must provide an email"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Haha... very funny. That's not a valid email."
        else:
            exists = self.filter(email=postData['email'])
            if len(exists) > 0:
                errors['email'] = "There is already a user with this email"

        if len(postData['password']) < 1:
            errors['password']="You must provide a password"
        elif len(postData["password"]) < 8:
            errors['password']="Password must be at least 8 characters"
        elif not any(c.isdigit() for c in postData['password']) or not any(c.isupper() for c in postData['password']):
            errors['password']="I know this is annoying, but your password must contain at least one number and one upper case"

        if len(postData['confirm']) < 1:
            errors['confirm']="You must provide a password confirmation"
        elif postData['confirm']!=postData['password']:
            errors['confirm']="The password confirmation did not match the password"
        return(errors)


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"< User object: {self.first_name} {self.last_name}>"
