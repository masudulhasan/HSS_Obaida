from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from common.models import Category, Author


# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=500)
    presenter = models.ForeignKey(Author)
    category = models.ManyToManyField(Category)
    location = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=5000, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    registration_limit = models.PositiveSmallIntegerField(null=True,
                                                          blank=True, default=10)
    fee = models.DecimalField(max_digits=255, decimal_places=2, default=0, null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def available_seats(self):
        return self.registration_limit - self.registration_set.count()

    @property
    def is_registration_open(self):
        return self.available_seats != 0 and self.start_time > now()

    @property
    def duration(self):
        time_diff = self.end_time - self.start_time
        return time_diff.total_seconds()/3600  # difference in hour

    class Meta:
        ordering = ('start_time',)
        get_latest_by = 'start_time'


class Registration(models.Model):
    event = models.ForeignKey(Event)
    attendee = models.ForeignKey(User)
    skype_id = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.attendee.username

    class Meta:
        unique_together = ["event", "attendee"]
        ordering = ('created',)
