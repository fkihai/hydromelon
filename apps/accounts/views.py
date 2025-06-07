from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated


from apps.accounts.serializers import AccountSerializer
from shared.utils.responses import ResponseHelper as res
from shared.utils.permissions import HasAPIKey


# Create your views here.
class RegisterView(APIView):
    permission_classes = [HasAPIKey]

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return res.success(
                data=serializer.data,
                message="user created successfully",
                status_code=status.HTTP_201_CREATED
            )
            
        return res.failed(
            message="Data is invalid",
            status_code=status.HTTP_400_BAD_REQUEST,
            errors=serializer.errors
        )


class UserView(APIView):
    permission_classes = [HasAPIKey, IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return res.success(
            data= {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        )
    
