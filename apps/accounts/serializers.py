from rest_framework import serializers
from .models import CustomUser

from apps.accounts.models import CustomUser

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username","email","password"] # must fill

        # not shown on json response
        extra_kwargs = {'password' : {'write_only' : True}} 
    
    
    def create(self, validate_data):
        return CustomUser.objects.create_user(**validate_data)
    
        