from django.db import models


class Cars(models.Model):
    id_car = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'cars'

