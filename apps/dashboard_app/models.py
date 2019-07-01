from django.db import models
import re 

class User_Validator(models.Manager):
     # validate fname and last name
    def validate_name(self, postData):
        errors = {}
        if len(postData['fname'].strip()) < 2:
            errors['fname_len'] = 'first name must be at least 2 characters'

        if len(postData['lname'].strip()) < 2:
            errors['lname_len'] = 'last name must be at least 2 characters'

        reg = re.compile(r'^[a-zA-Z]+$')
        if not reg.match(postData['fname'].strip()):
            errors['fname_type'] = 'first name must be all letters'

        if not reg.match(postData['lname'].strip()):
            errors['lname_type'] = 'last name must be all letters'

        return errors


    def validate_username(self, username):
        errors = {}
        if len(username) < 2 or len(username) > 30:
             errors['username'] = 'first name must be at least 2 characters or less than 30 characters'
        return errors


    # validate pw_hash
    def validate_pw(self, postData):
        errors = {}
        if len(postData['password']) < 8:
            errors['pw_len'] = 'password must be at least 8 characters long'

        if 'repeat-pass' in postData and postData['password'] != postData['repeat-pass']:
            errors['confirm'] = 'password did not confirm!!'

        return errors


    # validate email
    def validate_email(self, em):
        errors = {}
        Email_Regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not Email_Regex.match(em) or len(em) < 1:
            errors['email'] = 'not an email format'
        return errors




class User(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = User_Validator()

    def __repr__(self):
        return f'{self.username}'

    
class Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='messages')

    def __repr__(self):
        return f'{self.message}'


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments')
    message = models.ForeignKey(Message, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'{self.comment}'
