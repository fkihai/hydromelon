import os
import uuid
import torch
import torchvision

from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files.base import ContentFile

from torchvision.transforms import functional as F
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_Weights
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

class MelonRipenessDetector:
    
    COCO_CLASSES = {
        0: "Background",
        1: "Matang",
        2: "Mentah",
        3: "Setengah Matang"
    }
    
    def __init__(self, num_classes=4, threshold=0.5):
        self.num_classes = num_classes
        self.threshold = threshold
        self.device = torch.device('cpu')
        self.model = None
            
    def _getModel(self):
        weights = FasterRCNN_ResNet50_FPN_Weights.DEFAULT
        model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights=weights)
        in_features = model.roi_heads.box_predictor.cls_score.in_features
        model.roi_heads.box_predictor = FastRCNNPredictor(in_features, self.num_classes)
        return model

    def load_model(self, filename):
        model_path = os.path.join('apps', 'prediction', 'ml', filename)
        model = self._getModel()
        state_dict = torch.load(model_path, map_location=self.device)
        model.load_state_dict(state_dict)
        model.to(self.device)
        model.eval()
        self.model = model

                
    def load_image(self, image_path):
        image = Image.open(image_path).convert("RGB")
        image_tensor = F.to_tensor(image).unsqueeze(0)
        return image_tensor, image
    
    def predict(self, image_tensor):
        if self.model is None:
            raise ValueError("Model belum di-load. Panggil .load_model() terlebih dahulu.")
        with torch.no_grad():
            predictions = self.model(image_tensor)
        return predictions
        
    def get_classname(self, class_id):
        return self.COCO_CLASSES.get(class_id, "Unknown")
    
    def draw_box(self, image, prediction, fig_size=(10,10)):
        data = None # for pyload message response
        
        # validate prediction
        if not prediction or not prediction[0].get('boxes') is not None:
            return {
                'predictions': None,
                'score': None,
                'image': None,
                'errors': 'Prediction failed or returned no results.'
            }

        
        boxes = prediction[0]['boxes'].cpu().numpy()
        labels = prediction[0]['labels'].cpu().numpy()
        scores = prediction[0]['scores'].cpu().numpy()
                
        image_draw = image.copy()
        draw = ImageDraw.Draw(image_draw)

        for box, label, score in zip(boxes, labels, scores):
            if score > self.threshold:
                x_min, y_min, x_max, y_max = box
                class_name = self.get_classname(label)
                data = {
                    'predict' : class_name,
                    'score' : round(float(score),2),
                }
                draw.rectangle([x_min, y_min, x_max, y_max], outline='red', width=2)
                draw.text((x_min, y_min), f"{class_name} ({score:.2f})", fill='red')
        
        
        buffer = BytesIO()
        image_draw.save(buffer, format='JPEG')
        buffer.seek(0)
        
        random_name = f"{uuid.uuid4()}.jpg"
        django_file = ContentFile(buffer.read(), name=random_name)
                   
        return {
            'predictions' : data['predict'],
            'score' : data['score'],
            'image' : django_file,
            'errors': None
        }
        


    
    