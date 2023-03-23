from django.db import models

# Create your models here.
class UserRegister(models.Model):
    FullName = models.CharField(max_length=100)
    Email = models.EmailField()
    Mobile = models.PositiveIntegerField()
    AdharNo = models.PositiveIntegerField()
    Address = models.TextField()
    DOB = models.DateField()
    Age = models.IntegerField()
    Gender = models.CharField(max_length=10)
    Image = models.ImageField(upload_to='media/User/',default=None)
    UserName = models.CharField(max_length=25)
    Password = models.CharField(max_length=25)
    
    def __str__(self):
        return self.FullName
    
class UserTransaction(models.Model):
    UserName = models.CharField(max_length=25)
    Date = models.DateField()
    TransactionAmount = models.FloatField(default=0)
    TotalAmount = models.FloatField(default=0)
    Action = models.CharField(max_length=25)
    Notifications = models.TextField()
    
    def __str__(self):
        return self.UserName