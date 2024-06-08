from django.db import models

# Create your models here.

class Users(models.Model):

    gender_choices = (('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others'))
    
    full_name = models.CharField(max_length = 255)
    gender = models.CharField(max_length = 255, choices=gender_choices)
    age = models.IntegerField()
    email = models.EmailField(unique = True)
    phoneno = models.CharField(max_length = 255)
    password = models.CharField(max_length=255)
    profile_pic = models.FileField(upload_to="patient_profiles", default="sad.jpg")

    def __str__(self):
        return self.full_name