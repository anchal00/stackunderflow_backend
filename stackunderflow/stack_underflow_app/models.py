from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import ASCIIUsernameValidator

class User(AbstractUser):
    username_validator = ASCIIUsernameValidator()

    username = models.CharField(
        'username',
        max_length=15,
        unique=True,
        help_text='Required. May contain only English letters, numbers, and @/./+/-/_ characters.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    first_name = models.CharField('first name', max_length=20, blank=False)
    last_name = models.CharField('last name', max_length=20, blank=True)
    email = models.EmailField('email address', unique=True, blank=False)
    profession = models.CharField('profession', max_length=50, blank=True)
    dob = models.DateField('date of birth', help_text='Date of birth in format YYYY-MM-DD', null=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
