from django.db import models


class Barrier(models.Model):
    id_barrier = models.BigAutoField(primary_key=True)
    url_barrier = models.CharField(max_length=255)
    name = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.url_barrier

    class Meta:
        db_table = 'barrier'

