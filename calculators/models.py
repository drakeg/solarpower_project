from django.db import models

class SolarSavingsInput(models.Model):
    current_energy_cost = models.DecimalField(max_digits=10, decimal_places=2)
    solar_system_cost = models.DecimalField(max_digits=10, decimal_places=2)
    solar_system_lifetime = models.PositiveIntegerField()