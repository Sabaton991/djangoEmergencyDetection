from django.db import models


class Timer(models.Model):
    id_timer = models.BigAutoField(primary_key=True)
    barrier_timer = models.DurationField()
    alert_timer = models.DurationField()

    def __str__(self):
        return self.id_timer

    class Meta:
        db_table = 'timer'
