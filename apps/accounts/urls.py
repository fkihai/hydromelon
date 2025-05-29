from django.urls import include, path

from apps.accounts.views import RegisterView
from apps.prediction.views import PredictionView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('predict/', PredictionView.as_view(), name='predict')
]
