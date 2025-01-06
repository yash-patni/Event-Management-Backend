from django.db import models

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=255)
    date=models.DateField()
    location=models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Attendee(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField()
    event=models.ForeignKey(Event, related_name='attendees', on_delete=models.CASCADE)

    def __str__(self):
        return self.name