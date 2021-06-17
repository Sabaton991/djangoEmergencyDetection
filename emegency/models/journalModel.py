from django.db import models
from .cameraModel import Camera
from .carsModel import Cars


class Journal(models.Model):
    id_journal = models.BigAutoField(primary_key=True)
    id_camera = models.ForeignKey(Camera, on_delete=models.SET_NULL, null=True, db_column='id_camera')
    opened_at = models.DateTimeField()
    id_car = models.ForeignKey(Cars, on_delete=models.SET_NULL, null=True, db_column='id_car')

    class Meta:
        db_table = 'journal'