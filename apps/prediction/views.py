from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from shared.utils.responses import ResponseHelper
from shared.utils.permissions import HasAPIKey

from .models import DataPredict
from .serializers import PredictImageSerializer, UploadImageSerializer
from .utils.predict import MelonRipenessDetector

class PredictionView(APIView):
    permission_classes = [HasAPIKey, IsAuthenticated]
    
    # TODO: receive image and predict
    def post(self,request):
        serializer = UploadImageSerializer(data=request.data)
        
        try:            
            if serializer.is_valid():
                image_file = serializer.validated_data["image"]
        
            rippenesDetector =MelonRipenessDetector()
            rippenesDetector.load_model('fasterrcnn_resnet50_epoch_9.pth')
            image_tensor, image = rippenesDetector.load_image(image_file)
            predictions = rippenesDetector.predict(image_tensor)
            data = rippenesDetector.draw_box(image,predictions)
            
            instance = DataPredict.objects.create(
                image = data['image'],
                prediction = data['predictions'],
                score = data['score']
            )
            
            serializer = PredictImageSerializer(instance)

            return ResponseHelper.success(
                message="Success Prediction",
                data=serializer.data
            )
        
        except Exception as e :
            return ResponseHelper.failed(
                message=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



