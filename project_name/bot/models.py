from django.db import models


class Bot(models.Model):
    """
    Model for the database table that stores the contents you want to post
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
