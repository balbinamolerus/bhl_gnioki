from django.db import models

# Create your models here.

CHAR_FIELD_LEN = 50


class Appointment(models.Model):
    name = models.CharField(max_length = CHAR_FIELD_LEN)
    day = models.CharField(max_length = CHAR_FIELD_LEN)
    time = models.CharField(max_length=CHAR_FIELD_LEN)
