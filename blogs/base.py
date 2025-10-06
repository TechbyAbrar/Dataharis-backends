from rest_framework import generics, status
from rest_framework.response import Response


class BaseAPIView(generics.GenericAPIView):
    """
    A reusable Base API View that ensures all responses follow a consistent format.
    """

    success_message = "Request successful"
    error_message = "Request failed"

    def format_response(self, success=True, message=None, data=None, status_code=status.HTTP_200_OK):
        return Response({
            "success": success,
            "message": message or (self.success_message if success else self.error_message),
            "data": data
        }, status=status_code)

    # Override DRF's default handlers to wrap responses automatically
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return self.format_response(data=response.data, message="Fetched successfully")

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return self.format_response(data=response.data, message="Created successfully", status_code=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return self.format_response(data=response.data, message="Retrieved successfully")

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return self.format_response(data=response.data, message="Updated successfully")

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.format_response(message="Deleted successfully", data=None)
