from django.db import models

class WebhookTransaction(models.Model):
    TRANSACTION_STATUS = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('failed', 'Failed'),
    ]
    yaya_id = models.CharField(max_length=36, unique=True)  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    created_at_time = models.BigIntegerField()
    timestamp = models.BigIntegerField()
    cause = models.TextField()
    full_name = models.CharField(max_length=255)
    account_name = models.CharField(max_length=255)
    invoice_url = models.URLField()
    signature = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=TRANSACTION_STATUS, default='pending')
    received_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'webhook_app'  
        indexes = [
            models.Index(fields=['yaya_id']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.yaya_id} - {self.amount} {self.currency}"
    
    