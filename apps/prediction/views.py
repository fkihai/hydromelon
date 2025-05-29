from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from shared.utils.responses import ResponseHelper
from shared.utils.permissions import HasAPIKey

from .utils.prediction import MelonRipenessDetector

class PredictionView(APIView):
    permission_classes = [AllowAny, HasAPIKey]
    
    # TODO: receive image and predict
    def post(self,request):
        try:
            rippenesDetector =MelonRipenessDetector()
            rippenesDetector.load_model('fasterrcnn_resnet50_epoch_9.pth')
            image_tensor, image = rippenesDetector.load_image('melon.jpg')
            predictions = rippenesDetector.predict(image_tensor)
            data = rippenesDetector.draw_box(image,predictions)
            return ResponseHelper.success(
                message="Success Prediction",
                data=str(data)
            )
        
        except Exception as e :
            return ResponseHelper.failed(
                message=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



