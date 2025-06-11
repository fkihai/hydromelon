
from rest_framework.permissions import BasePermission
from web.config import base

class HasAPIKey(BasePermission):
    
    def has_permission(self, request, view):
        api_key = request.headers.get('X-API-KEY')
        return api_key == base.API_KEY
    
    