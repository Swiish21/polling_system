"""
Importing necessary modules from Django.

* `models`: Django's database modeling module, providing classes for defining database tables.
* `timezone`: Django's timezone utilities module, providing functions for working with timezones.
"""
from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib import admin
# from datetime import datetime, timedelta
import datetime
# Create your models here.
class Question(models.Model):
    """
    A model representing a question.

    Attributes:
        question_text (str): The text of the question.
        pub_date (datetime): The date and time the question was published.

    Methods:
        __str__: Returns a string representation of the question.
        was_published_recently: Returns True if the question was published within the last day.

    Admin Interface:
        The `was_published_recently` method is displayed as a boolean field in the admin interface,
        with a description of "Published recently" and sorted by publication date.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently',
    )
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    """
    A model representing a choice for a question.

    Attributes:
        question (Question): The question this choice belongs to.
        choice_text (str): The text of the choice.
        votes (int): The number of votes for this choice.

    Relationships:
        question: A foreign key referencing the Question model, with a cascade delete behavior.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now