from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models


class Tag(models.Model):
    name = models.CharField("tag name", max_length=10, blank=False, null=False, unique=True, db_index=True)


class User(AbstractUser):
    username_validator = ASCIIUsernameValidator()

    username = models.CharField(
        "username",
        max_length=15,
        unique=True,
        help_text="Required. May contain only English letters, numbers, and @/./+/-/_ characters.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    first_name = models.CharField("first name", max_length=20, blank=False)
    last_name = models.CharField("last name", max_length=20, blank=True)
    email = models.EmailField("email address", unique=True, blank=False)
    profession = models.CharField("profession", max_length=50, blank=True)
    dob = models.DateField("date of birth", help_text="Date of birth in format YYYY-MM-DD", null=True)
    reputation_points = models.IntegerField("reputation points", default=0)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]


class PostType(models.Model):
    QUES = "QUESTION"
    ANS = "ANSWER"
    COMT = "COMMENT"

    POST_TYPES = [
        (QUES, "Question"),
        (ANS, "Answer"),
        (COMT, "Comment")
    ]

    name = models.CharField("post type", max_length=10, choices=POST_TYPES, default=QUES, unique=True)


class Question(models.Model):
    OPEN = "OPEN"
    CLOSED = "CLOSED"

    QUESTION_STATUS = [
        (OPEN, "Open"),
        (CLOSED, "Closed"),
    ]

    NOT_CLEAR = "NOT_CLEAR"
    DUPLICATE = "DUPLICATE"
    INVALID = "INVALID"

    QUESTION_CLOSING_REMARK = [
        (NOT_CLEAR, "Not clear"),
        (DUPLICATE, "Duplicate question"),
        (INVALID, "Not a valid question"),
    ]

    title = models.CharField("question title", max_length=60, blank=False, null=False)
    description = models.TextField("detailed description of the question/issue", blank=True, null=True)
    author = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL)
    viewcount = models.IntegerField("number of times question is viewed", null=False, default=0)
    status = models.CharField("question status", max_length=7, choices=QUESTION_STATUS, default=OPEN)
    closing_remark = models.CharField(
        "question closing remark",
        max_length=10,
        choices=QUESTION_CLOSING_REMARK,
        null=True
    )
    created_at = models.DateTimeField("question posted at", auto_now_add=True)
    updated_at = models.DateTimeField("question updated at", auto_now=True)
    tags = models.ManyToManyField(Tag)

    @property
    def upvotes(self):
        return len(Votes.objects.filter(post_id=self.id,
                                        post_type=PostType.objects.get(name=PostType.QUES),
                                        upvote=True))

    @property
    def downvotes(self):
        return len(Votes.objects.filter(post_id=self.id,
                                        post_type=PostType.objects.get(name=PostType.QUES),
                                        downvote=True))

    @property
    def accepted_answer(self):
        try:
            return Answer.objects.get(question=self, is_accepted=True)
        except Answer.DoesNotExist:
            pass
        return None


class Answer(models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    answer_body = models.TextField("answer body", blank=False)
    created_at = models.DateTimeField("answer posted at", auto_now_add=True)
    updated_at = models.DateTimeField("answer updated at", auto_now=True)
    is_accepted = models.BooleanField("is accepted answer", default=False)

    @property
    def upvotes(self):
        return len(Votes.objects.filter(post_id=self.id,
                                        post_type=PostType.objects.get(name=PostType.ANS),
                                        upvote=True))

    @property
    def downvotes(self):
        return len(Votes.objects.filter(post_id=self.id,
                                        post_type=PostType.objects.get(name=PostType.ANS),
                                        downvote=True))


class Comment(models.Model):
    body = models.CharField("comment body", max_length=100, blank=False, null=False)
    post_id = models.BigIntegerField("post id")
    post_type = models.ForeignKey(to=PostType, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField("comment posted at", auto_now_add=True)
    updated_at = models.DateTimeField("comment updated at", auto_now=True)

    @property
    def upvotes(self):
        return len(Votes.objects.filter(post_id=self.id,
                                        post_type=PostType.objects.get(name=PostType.COMT),
                                        upvote=True))

    @property
    def downvotes(self):
        return len(Votes.objects.filter(post_id=self.id,
                                        post_type=PostType.objects.get(name=PostType.COMT),
                                        downvote=True))


class Votes(models.Model):
    class Meta:
        unique_together = (("post_id", "post_type", "user"),)

    post_id = models.BigIntegerField("post id", db_index=True)
    post_type = models.ForeignKey(to=PostType, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    upvote = models.BooleanField("Is upvote")
    downvote = models.BooleanField("Is downvote")
