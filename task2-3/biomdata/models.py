# myapp/models.py

from django.db import models

class Taxonomy(models.Model):
    name = models.CharField(max_length=255)
    tax_id = models.IntegerField()
    abundance_score = models.FloatField()
    relative_abundance = models.FloatField()
    unique_matches_frequency = models.IntegerField()

    def __str__(self):
        return self.name
