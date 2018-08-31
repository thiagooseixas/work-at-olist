from django.db import models


class Call(models.Model):
    started_at = models.DateTimeField(auto_now_add=False)
    ended_at = models.DateTimeField(auto_now_add=False)
    source = models.IntegerField()
    destination = models.IntegerField()

    class Meta:
        ordering = ('started_at',)


class TelephoneBill(models.Model):
    mount = models.DateTimeField(
        auto_now_add=False, unique_for_month='started_at')
    year = models.DateTimeField(
        auto_now_add=False, unique_for_year='started_at')
    telephone = models.IntegerField()


class CallRecord(models.Model):
    type = models.CharField(),
    timestamp = models.DateTimeField(auto_now_add=False),
    call_id = models.IntegerField(),
    source = models.IntegerField(blank=True, null=True)
    destination = models.IntegerField(blank=True, null=True)
