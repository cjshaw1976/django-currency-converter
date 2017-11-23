from django.db import models
import datetime

# For saving each days data
class rates(models.Model):
    date = models.DateField(unique=True)
    curencyAUD = models.FloatField(null=True);
    curencyCAD = models.FloatField(null=True);
    curencyCHF = models.FloatField(null=True);
    curencyCNY = models.FloatField(null=True);
    curencyEUR = models.FloatField(null=True);
    curencyGBP = models.FloatField(null=True);
    curencyNZD = models.FloatField(null=True);
    curencyZAR = models.FloatField(null=True);

    def __str__(self):
        return self.date.strftime("%A %d. %B %Y")
