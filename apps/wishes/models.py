from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from datetime import date, datetime
from django.db.models import Count
import re
import bcrypt

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r'^[a-zA-Z0-9]{3,}$')

class UserManager(models.Manager):
    def validate(self, postData):
        count = 0
        errors = []

        if not name_regex.match(postData['name']):
            errors.append("Name must be at least 3 characters and composed of only letters and numbers")
            count += 1
        if not name_regex.match(postData['username']):
            errors.append("Username must be at least 3 characters and composed of only letters and numbers")
            count += 1
        if len(self.filter(username=postData['username'])) > 0:
            errors.append("Registration is invalid. Username is already registered!")
            count += 1
        if not email_regex.match(postData['email']):
            errors.append("Email not valid. Please use name@host.com format")
            count += 1
        if len(User.objects.filter(email = postData['email'])) > 0:
            errors.append("Email in use. Please choose another")
            count += 1
        if postData['pass1'] != postData['pass2']:
            errors.append("Passwords do not match")
            count += 1
        if len(postData['pass1']) | len(postData['pass2']) < 7:
            errors.append("Password must be at least 8 characters")
            count += 1
        try:
            startdate = datetime.strptime(postData['startdate'], '%Y-%m-%d')
            if startdate >= datetime.now():
                errors.append("Invalid: Hire date is in the future")
                count += 1
        except:
            errors.append('Missing Hire date')
            count += 1

        if count > 0:
            return (False, errors)
        else:
            password = postData['pass1']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

            newuser= User.objects.create(name = postData['name'], username = postData['username'], pw_hash = pw_hash, email = postData['email'], startdate = postData['startdate'])
            return (True, newuser)

    def login(self, postData):
        count = 0
        errors = []
        user = User.objects.filter(username = postData['lusername'])
        if len(user) < 1:
            errors.append("Not a registered Username")
            count +=1
        if count > 0:
            return (False, errors)

        else:
            if bcrypt.hashpw(postData['lpassword'].encode(), user[0].pw_hash.encode()) == user[0].pw_hash:
                return (True, user[0])
            else:
                errors.append('Password does not match')
                return (False, errors)

class WishManager(models.Manager):
    def additem(self, postData, user):
        errors = []
        count = 0
        if len(postData['wishitem']) < 1:
            errors.append("Must include item name")
            count +=1
        if len(Wish.objects.filter(wishitem = postData['wishitem'])) > 0:
            errors.append("Item already registered. Please choose another")
            count += 1

        if count > 0:
            return (False, errors)

        elif count == 0:
            wish = Wish.objects.create(wishitem = postData['wishitem'], addby=user)
            wish.share.add(user)
            return (True, 'Item Added to Wishlist')

    def shareitem(self, wish_id, user):
        wish = Wish.objects.get(id=wish_id)
        wish.share.add(user)
        return (True, "Successfully added an item")
        

class User(models.Model):
    name = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100)
    pw_hash = models.CharField(max_length = 250)
    startdate = models.DateField(auto_now = False, blank = True)
    email = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)
    objects = UserManager()

class Wish(models.Model):
    wishitem = models.CharField(max_length = 100)
    addby = models.ForeignKey(User)
    share = models.ManyToManyField(User, related_name='care')
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)
    objects = WishManager()
