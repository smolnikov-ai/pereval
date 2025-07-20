from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import PerevalSerializer, PerevalInfoSerializer, PerevalUpdateSerializer


class SubmitData(APIView):
    """
    Representation for operations with information about passes.
    The class provides methods for obtaining, creating, and partially updating information about passes.

    Methods:
        get(request, pk): returns detailed information about a pass by its pk
        post(request): creates a new pass object based on the received data
        patch(request, pk): partially updates an existing pass if its status is 'new'
    """

    def post(self, request):
        serializer = PerevalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request, pk):
    #         object = Pereval.objects.get(pk=pk)
    #         return Response(PerevalInfoSerializer(object).data)

    def patch(self, request, pk):
        object = Pereval.objects.get(pk=pk)

        if object.status == 'new':
            serializer = PerevalUpdateSerializer(object, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'state': '1',
                                 'message': 'Editing a database record is a success'})
            return Response({'state': '0',
                             'message': 'An error occurred while editing a database record. The form is not valid'})
        else:
            return Response({'state': '0',
                             'message': 'Changes are not allowed. Record status is not new'})