# models.py
from django.db import models

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected')
]

class Certificate(models.Model):
    name = models.CharField(max_length=100)
    issued_to = models.CharField(max_length=100)
    description = models.TextField()
    email = models.EmailField()
    cert_hash = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    rejection_reason = models.TextField(blank=True, null=True) 


    def __str__(self):
        return f"{self.issued_to} - {self.status}"
