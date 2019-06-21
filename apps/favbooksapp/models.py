from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#-------------------------------------------------------------------------------
#User
#-------------------------------------------------------------------------------

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "Invalid First Name! - Must be 2 characters long"
        if not (postData['first_name'].isalpha()) == True:
            errors['first_name'] = "Invalid First Name! - Can only contain alphabetic characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Invalid Last Name! - Must be 2 characters long"
        if not (postData['last_name'].isalpha()) == True:
            errors['last_name'] = "Invalid Last Name! - Can only contain alphabetic characters"
        
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email Address!"
        emailAlreadyExists = User.objects.filter(DBemail = postData['email']).exists()
        if (emailAlreadyExists):
            errors['email'] = "Email already in system"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        if postData['password'] != postData['pwconfirm']:
            errors['confirmpw'] = "Password and Confirm Password must match"
        return errors

    def login_validator(self, postData):
        errors = {}
        loginemailAlreadyExists = User.objects.filter(DBemail = postData['emailLogin']).exists()
        if not (loginemailAlreadyExists):
            errors['loginemail'] = "Failure to login"
        user = User.objects.get(DBemail=postData["emailLogin"])
        pw_to_hash = postData["passwordLogin"]
        if not bcrypt.checkpw(pw_to_hash.encode(), user.DBpassword.encode()):
            errors['loginemail'] = "Failure to login"
        # if len(postData['loginemail']) == 0:
        #     errors['loginemail'] = "Failure to login"
        return errors




class User(models.Model):
    DBfirst_name = models.CharField(max_length = 255)
    DBlast_name = models.CharField(max_length = 255)
    DBemail = models.CharField(max_length = 255)
    DBpassword = models.CharField(max_length = 255)
    #liked_books = a list of books a given user likes
    #books_uploaded = a list of books uploaded by a given user
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return f"<User object: {self.DBfirst_name} {self.DBlast_name} {self.DBemail} {self.DBpassword} ({self.id})>"

#-------------------------------------------------------------------------------
#Book
#-------------------------------------------------------------------------------

class BookManager(models.Manager):
    def basic_validator_add(self, postData):
        errors = {}



        if not len(postData['form_add_description']) > 5 :
            errors['desc'] = "Description should be more than 5 characters" 
        
        if not len(postData['form_add_title']) > 1:
            errors['title'] = "Title should be at least 1 characters"
        
        return errors

    def basic_validator_edit(self, postData):
        errors = {}
        if len(postData['form_edit_title']) < 1:
            errors['title'] = "Title should be at least 1 characters"
        if len(postData['form_edit_description']) < 5 :
            errors['desc'] = "Description should be more than 5 characters"

        return errors

class Book(models.Model):
    DBtitle = models.CharField(max_length = 255)
    DBdesc = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded")
    users_who_like = models.ManyToManyField(User, related_name = "liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
    def __repr__(self):
        return f"<User object: {self.DBtitle} {self.DBdesc} ({self.id})>"
