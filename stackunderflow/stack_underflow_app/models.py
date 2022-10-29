from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField('tag name', max_length=10, blank=False, null=False)
    description = models.CharField('description of the tag', max_length=20, blank=True)


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


class Question(models.Model):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'

    QUESTION_STATUS = [
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
    ]

    NOT_CLEAR = 'NOT_CLEAR'
    DUPLICATE = 'DUPLICATE'
    INVALID = 'INVALID'

    QUESTION_CLOSING_REMARK = [
        (NOT_CLEAR, 'Not clear'),
        (DUPLICATE, 'Duplicate question'),
        (INVALID, 'Not a valid question'),
    ]

    title = models.CharField('question title', max_length=60, blank=False, null=False)
    description = models.TextField('detailed description of the question/issue', blank=True, null=True)
    upvotes = models.IntegerField('upvotes', null=False, default=0)
    downvotes = models.IntegerField('downvotes', null=False, default=0)
    viewcount = models.IntegerField('number of times question is viewed', null=False, default=0)
    status = models.CharField('question status', max_length=7, choices=QUESTION_STATUS, default=OPEN)
    closing_remark = models.CharField('question closing remark', max_length=10, choices=QUESTION_CLOSING_REMARK, null=True)
    created_at = models.DateTimeField('question posted at', auto_now_add=True)
    updated_at = models.DateTimeField('question updated at', auto_now=True)


class Answer(models.Model):
    question = models.OneToOneField(to=Question, on_delete=models.CASCADE)
    answer_body = models.TextField('answer body', blank=False)
    upvotes = models.IntegerField('upvotes', null=False, default=0)
    downvotes = models.IntegerField('downvotes', null=False, default=0)
    created_at = models.DateTimeField('answer posted at', auto_now_add=True)
    updated_at = models.DateTimeField('answer updated at', auto_now=True)

