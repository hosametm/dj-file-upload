from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import UploadedFile
from .serializers import UploadedFileSerializer

class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        if file.size > 5 * 1024 * 1024:  # 5 MB limit
            return Response({"error": "File size exceeds 5 MB limit."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UploadedFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileListView(APIView):
    def get(self, request, *args, **kwargs):
        file_type = request.query_params.get('file_type', None)
        if file_type:
            files = UploadedFile.objects.filter(file_type=file_type)
        else:
            files = UploadedFile.objects.all()

        serializer = UploadedFileSerializer(files, many=True)
        return Response(serializer.data)

class FileRetrieveView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            file = UploadedFile.objects.get(pk=pk)
            serializer = UploadedFileSerializer(file)
            return Response(serializer.data)
        except UploadedFile.DoesNotExist:
            return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)
