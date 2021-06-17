from django.db import models
from .barrierModel import Barrier


class Camera(models.Model):
    id_camera = models.BigAutoField(primary_key=True)
    url_camera = models.CharField(max_length=255)
    id_barrier = models.ForeignKey(Barrier, on_delete=models.SET_NULL, null=True, db_column='id_barrier')
    description = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'camera'
