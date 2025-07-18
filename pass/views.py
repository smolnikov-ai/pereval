from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import PerevalSerializer, PerevalInfoSerializer, PerevalUpdateSerializer


class SubmitData(APIView):

    def get(self, request, pk):
        object = Pereval.objects.get(pk=pk)
        return Response(PerevalInfoSerializer(object).data)

    def post(self, request, *args, **kwargs):
        serializer = PerevalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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