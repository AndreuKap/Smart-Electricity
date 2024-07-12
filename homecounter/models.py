from django.db import models

class Counters(models.Model):
    identifier = models.CharField(max_length = 64)
    power = models.FloatField()
    datetime = models.DateTimeField()



class Languages(models.Model):
    key = models.CharField(max_length = 20)
    ua = models.CharField(max_length = 50)
    ru = models.CharField(max_length = 50, null=True)
    en = models.CharField(max_length = 50, null=True)


class Cost(models.Model):
    cost_dey = models.FloatField()
    cost_night = models.FloatField()