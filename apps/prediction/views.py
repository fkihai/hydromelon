from PIL import Image
from io import BytesIO
from torchvision.transforms import functional as F

from django.shortcuts import render
from django.core.files.base import ContentFile

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from shared.utils.responses import ResponseHelper
from shared.utils.permissions import HasAPIKey

from .models import DataPredict
from .serializers import PredictImageSerializer, UploadImageSerializer
from .utils.predict import MelonRipenessDetector


rippenesDetector =MelonRipenessDetector()   
rippenesDetector.load_model('fasterrcnn_resnet50_epoch_9.pth')

class PredictionView(APIView):
    permission_classes = [HasAPIKey, IsAuthenticated]
    
    # TODO: receive image and predict
    def post(self,request):
        serializer = UploadImageSerializer(data=request.data)
        
        try:            
            if serializer.is_valid():
                image_file = serializer.validated_data["image"]

                # Load image
                img = Image.open(image_file).convert("RGB")
                orig_w, orig_h = img.size

                target_w, target_h = 800, 450
                ratio = min(target_w / orig_w, target_h / orig_h)
                new_w, new_h = int(orig_w * ratio), int(orig_h * ratio)

                # Resize while maintaining aspect ratio
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

                # Hitung padding
                pad_left = (target_w - new_w) // 2
                pad_top = (target_h - new_h) // 2
                pad_right = target_w - new_w - pad_left
                pad_bottom = target_h - new_h - pad_top

                # Pad ke ukuran 800x450
                padding = (pad_left, pad_top, pad_right, pad_bottom)
                img = F.pad(img, padding, fill=0)  # padding hitam

                # Simpan sebagai ContentFile (untuk Django)
                buffer = BytesIO()
                img.save(buffer, format='JPEG')
                buffer.seek(0)
                resized_image = ContentFile(buffer.read(), name=image_file.name)
                
        
            image_tensor, image = rippenesDetector.load_image(resized_image)
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
            print(e)
            return ResponseHelper.failed(
                message=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get(self,request):
        predictions = DataPredict.objects.all().order_by("-predict_at")
        serializer = PredictImageSerializer(predictions, many=True)
        return ResponseHelper.success(
            data=serializer.data
        )


