from django.db import models

# Create your models here.
class DataPredict(models.Model):
    image = models.ImageField(upload_to='predict/')
    prediction = models.CharField(max_length=20)
    score = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    predict_at = models.DateTimeField(auto_now_add=True)
    