from django.db import models

class Client(models.Model):
    Id = models.AutoField(primary_key=True)
    First_Name = models.CharField(max_length=255)
    Last_Name = models.CharField(max_length=255)
    Phone_Numder = models.CharField(max_length=255)
    Login = models.CharField(max_length=25)
    Password = models.CharField(max_length=25)
    Massanger = models.CharField(max_length=255)
    Photo_Profile = models.ImageField()
    Jwt_Token = models.UUIDField(unique=True)
    Tarife = models.CharField(max_length=255)
    Referal_Url = models.ForeignKey("Referal", on_delete=models.CASCADE, null=True)
    Tarif_Active = models.BooleanField()

class Tarife(models.Model):
    Id = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=255)
    Description = models.TextField()
    Price = models.FloatField()

class Referal(models.Model):
    Id = models.AutoField(primary_key=True)
    Url = models.CharField(max_length=255)

class News(models.Model):
    Id = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=255)
    Description = models.TextField()
    User_Uuid = models.ForeignKey("Client", on_delete=models.CASCADE)
    Created_Date = models.DateTimeField()
        
class StackOverflow(models.Model):
    Id = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=255)
    Description = models.TextField()
    User_Uuid = models.ForeignKey("Client", on_delete=models.CASCADE)
    Created_Date = models.DateTimeField()
    Category = models.ForeignKey("Newness_Category", on_delete=models.CASCADE)

class Newness_Category(models.Model):
    Id = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=255)

class Config(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Description = models.TextField()
    Tg_Id = models.CharField(max_length=255)
    Parameters = models.JSONField()

class Analytics(models.Model):
    channel = models.CharField(max_length=100)
    messages_count = models.IntegerField(default=0)
    members_count = models.IntegerField(default=0)
    keyword_matches = models.IntegerField(default=0)
    relevance = models.FloatField(default=0)

    def __str__(self):
        return self.channel
