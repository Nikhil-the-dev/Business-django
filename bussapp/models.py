from django.db import models
class Vehicle_list(models.Model):
    Add_vehicle_numbers = models.CharField(max_length=255)
    Date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.Add_vehicle_numbers
    
class Register(models.Model):
    Fullname = models.CharField(max_length=255)
    Email = models.EmailField(max_length=255)
    Password = models.CharField(max_length=255)
    
    def __str__(self):
        return self.Fullname + '' + '' + self.Email

    
class Vehicle(models.Model):
    Vehicle_number = models.CharField(max_length=255)
    Fuel_date = models.DateField(auto_now_add=True)
    Fuel_Ltr = models.FloatField(max_length=255)
    Fuel_rate_per_ltr = models.FloatField(max_length=255)
    Total_fuel_price = models.FloatField(max_length=255)
    Remark = models.TextField()
    
    def __str__(self):
        return self.Vehicle_number
