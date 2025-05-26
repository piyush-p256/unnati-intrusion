from django.db import models

class TrafficLog(models.Model):
    ip_address   = models.GenericIPAddressField()
    timestamp    = models.DateTimeField(auto_now_add=True)
    attack_type = models.CharField(max_length=50, default="Unknown")
    blocked      = models.BooleanField(default=False)
    raw_data     = models.JSONField()

    def __str__(self):
        return f"{self.timestamp} | {self.ip_address} | {self.attack_type}"
