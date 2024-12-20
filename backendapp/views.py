from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework import status
from .serializers import (
    MedecinSerializer, 
    PatientSerializer, 
    LaborantinSerializer, 
    InfirmierSerializer, 
    RadiologueSerializer
)
from .models import User, Medecin, Patient, Infirmier, Laborantin, Radiologue

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Authenticate the user
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)  # Log in the user (sets the session)

        # Get or create an authentication token
        token, created = Token.objects.get_or_create(user=user)

        # Prepare response data
        response_data = {
            'token': token.key,
            'username': user.username,
            'role': user.role,
        }

        # Determine the user's specific role and fetch related data
        if user.role == 'Patient':
            try:
                patient = Patient.objects.get(pk=user.pk)
                response_data['data'] = PatientSerializer(patient).data
            except Patient.DoesNotExist:
                return Response({'message': 'Patient data not found'}, status=status.HTTP_400_BAD_REQUEST)

        elif user.role == 'Medecin':
            try:
                medecin = Medecin.objects.get(pk=user.pk)
                response_data['data'] = MedecinSerializer(medecin).data
            except Medecin.DoesNotExist:
                return Response({'message': 'Medecin data not found'}, status=status.HTTP_400_BAD_REQUEST)

        elif user.role == 'Laborantin':
            try:
                laborantin = Laborantin.objects.get(pk=user.pk)
                response_data['data'] = LaborantinSerializer(laborantin).data
            except Laborantin.DoesNotExist:
                return Response({'message': 'Laborantin data not found'}, status=status.HTTP_400_BAD_REQUEST)

        elif user.role == 'Infirmier':
            try:
                infirmier = Infirmier.objects.get(pk=user.pk)
                response_data['data'] = InfirmierSerializer(infirmier).data
            except Infirmier.DoesNotExist:
                return Response({'message': 'Infirmier data not found'}, status=status.HTTP_400_BAD_REQUEST)

        elif user.role == 'Radiologue':
            try:
                radiologue = Radiologue.objects.get(pk=user.pk)
                response_data['data'] = RadiologueSerializer(radiologue).data
            except Radiologue.DoesNotExist:
                return Response({'message': 'Radiologue data not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Return the final response
        return Response(response_data, status=status.HTTP_200_OK)

    else:
        return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
