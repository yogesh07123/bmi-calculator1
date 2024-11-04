from django.db import models




# Create your models here.
class bmidata(models.Model):
    name = models.CharField(max_length=100)
    height = models.CharField(max_length=100)  
    weight = models.CharField(max_length=100)  
    bmi = models.CharField(max_length=100) 
    user_id = models.CharField(max_length=100,unique=True) 

