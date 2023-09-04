
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,parser_classes
from .serializers import FileShareSerializer
from rest_framework.parsers import FormParser,MultiPartParser,FileUploadParser
from .models import FileShare
from ezapp.models import CustomUser
from django.http import FileResponse
from django.conf import settings
# Create your views here.
import os
@api_view(['POST'])
@parser_classes([MultiPartParser],)
def uploadFile(request):
    try:
        auth = request.META.get('HTTP_AUTHORIZATION')
        token = auth.split(' ')[1]
        user = CustomUser.objects.filter(loginToken = token)
        if user:
            print(request.data)
            file = request.FILES["file"]
            upload_path = f'uploads/{request.FILES["file"].name}' 
            file_meta = request.FILES["file"].name                                               
            with open(upload_path, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
                FileShareSerializer['file_meta']=request.FILES["file"].name
                FileShareSerializer.save()
                return Response('success',status=status.HTTP_201_CREATED)
            return Response(file_serializer.errors)
        else:
            return Response("Invalid token login again")
    except Exception as e :
        print(e)
        return Response('error',status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def listAllUploadedFIle(request):
    auth = request.META.get('HTTP_AUTHORIZATION') 
    # check for none value in auth
    if not auth:                
        return Response("Enter valid token")
    token = auth.split(' ')[1]
    user = CustomUser.objects.filter(loginToken = token)
    if user:
        file = FileShare.objects.all()
        serializer = FileShareSerializer(file,many=True)
        return Response(serializer.data)
    else:
        return Response("Invalid token login again")


@api_view(['GET'])
def downloadFile(request):
    auth = request.META.get('HTTP_AUTHORIZATION')
    token = auth.split(' ')[1]
    user = CustomUser.objects.filter(loginToken = token)
    if user:
        file_name = request.GET.get('file_name')
        file = FileShare.objects.get(file_meta = file_name) 
        file_path=f'/uploads/{file_name}'
        if not file:
            return Response("File not found")
        with open(file_path, 'rb') as file_content:
                response = FileResponse(file_content)
                response['Content-Disposition'] = f'attachment; filename="{file.file.name}"'
                return response
    else:
        return Response("Invalid token login again")