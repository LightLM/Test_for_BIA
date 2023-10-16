from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=50)
    hours = models.BigIntegerField(default=0)


class Shift(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
