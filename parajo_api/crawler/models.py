from django.db import models

# Create your models here.
class Furits(models.Model):
    name = models.CharField(max_length=50)
    descript = models.TextField()
    price = models.FloatField()
    quantity = models.IntegerField()
    cdate = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return  self.name

class CarInfo(models.Model):
    seq = models.AutoField(primary_key=True)
    carid = models.CharField(max_length=50)
    info = models.CharField(max_length=50)
    price = models.IntegerField()
    accident = models.CharField(max_length=50)
    site = models.CharField(max_length=20)

    class Meta:
        db_table = "web_scraped_car_info" # table 실제이름 직접입력할경우 
    def __str__(self):
        return  self.info

        
