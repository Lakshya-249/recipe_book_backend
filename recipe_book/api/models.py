from email.mime import image
from random import choices
from django.db import models

# Create your models here.
class Chef(models.Model):
    chef_id = models.AutoField(primary_key=True)
    chef_name = models.CharField(max_length = 150)
    email = models.CharField(max_length = 250,unique=True)
    password = models.CharField(max_length = 150)
    username = models.CharField(max_length =130,unique=True)

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 150,choices = (('Main_Dishes','Main_Dishes'),
                                                        ('Dessert','Dessert'),
                                                        ('Drinks','Drinks'),
                                                        ('Side Dishes','Side Dishes'),
                                                        ('Appatizers','Appatizers')
                                                        ))

class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 150)
    image = models.CharField(max_length= 300)
    ingrediants = models.TextField()
    steps = models.TextField()
    chef = models.ForeignKey(Chef,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    comment = models.TextField()
    chef = models.ForeignKey(Chef,on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE)

