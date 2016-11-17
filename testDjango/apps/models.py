from django.db import models
from mongoengine import *

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField()



class User(Document):
    email = StringField(required=True)
    name = StringField()

    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)

class Inner(Document):
    name = StringField()
    l = ListField()

class Respondents(Document):
    cell_num = StringField(required=True)
    info = DictField()
    fixed_exp = DictField()
    call = DictField()
    msg = DictField()
    net = DictField()


    # inner = ReferenceField(Inner)



