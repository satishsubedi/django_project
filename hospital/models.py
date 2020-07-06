from django.db import models
from django.contrib.auth import get_user_model
UserModel = get_user_model()
from users.models import DoctorSpeciality

class Hospital(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    image = models.ImageField(null=True,blank=True,upload_to='media/images/hospitals/%Y-%m-%d/')
    created_by = models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name='hospital_created_by')
    created_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)


    def __str__(self):
        return self.name

class ExaminationType(models.Model):
    name = models.CharField(unique = True,max_length=50)
    status = models.BooleanField(default=False)
    rate = models.FloatField()
    reference_range=models.CharField(max_length=50)
    units=models.CharField(max_length=50)
    cpt_code=models.IntegerField()

    def __str__(self):
        return self.name
class PatientCheckupResult(models.Model):
    value=models.CharField(max_length=50)

    def __str__(self):
        return self.value









