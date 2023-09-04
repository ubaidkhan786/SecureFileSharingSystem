from django.urls import path
from .views import uploadFile,listAllUploadedFIle,downloadFile

urlpatterns = [
    path('uploadfile/', uploadFile, name='uploadfile'),
    path('filelist/',listAllUploadedFIle,name='filelist'),
    path('download/',downloadFile,name='download'),
]