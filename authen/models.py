from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
import jwt
from django.conf import settings
from datetime import datetime, timedelta

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, first_name,last_name,email,password):
        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email),first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email,password,first_name=None,last_name=None):
        if password is None:
            raise TypeError('Superusers must have a password.')

        admin = self.create_user(first_name,last_name,email,password)
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()
        return admin

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name=models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    contact_no = models.CharField(max_length=10,null=True,blank=True)
    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email
    @property
    def token(self):
        return self._generate_jwt_token()
    
    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=10)
        token = jwt.encode({
            'id': self.pk,
            'email': self.email,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token    



class Authmodel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True,blank=True)
    created_by = models.ForeignKey(User,related_name="%(class)s_created_by",on_delete=models.CASCADE,null=True,blank=True)
    modified_by = models.ForeignKey(User,related_name="%(class)s_modified_by",on_delete=models.CASCADE,null=True,blank=True)
    class Meta:
        abstract = True