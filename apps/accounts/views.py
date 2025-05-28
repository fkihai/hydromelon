from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from apps.accounts.serializers import AccountSerializer
from shared.utils.responses import ResponseHelper
from shared.utils.permissions import HasAPIKey


# Create your views here.
class RegisterView(APIView):
    permission_classes = [AllowAny, HasAPIKey]

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return ResponseHelper.success(
                data=serializer.data,
                message="user created successfully",
                status_code=status.HTTP_201_CREATED
            )
            
        return ResponseHelper.failed(
            message="Data is invalid",
            status_code=status.HTTP_400_BAD_REQUEST,
            errors=serializer.errors
        )

