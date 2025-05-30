from rest_framework import serializers
from .models import DataPredict


class UploadImageSerializer(serializers.Serializer):
    image = serializers.ImageField();

class PredictImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPredict
        fields = ['id','image','prediction','score','predict_at']

    
