from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PerevalSerializer


class SubmitData(APIView):

    def post(self, request, *args, **kwargs):
        serializer = PerevalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)