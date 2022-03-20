from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models


# Create your models here.

class Customer(models.Model):
    username = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)
    id = models.AutoField(primary_key=True)

    def str(self):
        return self.username


class Cars(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    id = models.CharField(max_length=200, primary_key=True)


class CarsCustomers(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car_id = models.CharField(max_length=200, primary_key=True)
