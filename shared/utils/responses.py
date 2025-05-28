from rest_framework.response import Response
from rest_framework import status

class ResponseHelper:
    @staticmethod
    def success(message=None, data=None, status_code=200):
        return Response({
            "success": True,
            "message": message,
            "data": data
        }, status=status_code)

    @staticmethod
    def failed(message=None, status_code=400, errors=None):
        return Response({
            "success": False,
            "message": message,
            "errors" : errors
        }, status=status_code)

        