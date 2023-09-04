from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .serializers import UserSerializer
from .models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
import uuid
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

@api_view(['POST'])
def registerUser(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['is_active']=False
            uutoken=str(uuid.uuid4())
            serializer.validated_data['uutoken']=uutoken
            serializer.save()
            url = send_emailconf(request.data.get('email'),uutoken)
            return Response(url,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])  
def verify_email(request,uutoken):

    profile_obj=CustomUser.objects.filter(uutoken=uutoken)
    print(profile_obj)
    print(uutoken)
    if not profile_obj:
        return Response('Invalid token please resend confirmation')
    profile_obj.is_active=True
    for obj in profile_obj:
        obj.is_active=True
        obj.save()
    return Response(request, 'Your account has been verified.',status=status.HTTP_200_OK)
    
@api_view(['POST'])
def userLogin(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user=None
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass
        if not user:
            user = authenticate(username=username,password=password)
        if user:
            token,_ =Token.objects.get_or_create(user=user)
            user.loginToken = str(token)
            user.save()
            return Response({'token':token.key},status=status.HTTP_200_OK)
        return Response({'error':'invalid credential'},status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def userLogout(request):
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

def send_emailconf(emails,uutoken):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/profile/verify/{uutoken}'
    url = 'http://127.0.0.1:8000/profile/verify/{uutoken}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [emails]
    send_mail(subject, message , email_from ,recipient_list )
    return url