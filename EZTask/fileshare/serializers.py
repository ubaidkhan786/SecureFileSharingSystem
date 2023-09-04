from rest_framework import serializers
from .models import FileShare

class FileShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileShare
        fields = '__all__'

        #fields  file name dalna add in model main bhi