from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LoginAPIView(APIView):
    def post(self, request):
        # Handle login logic
        return Response({'status': 'logged in'}, status=status.HTTP_200_OK)

class TwoFactorSetupAPIView(APIView):
    def post(self, request):
        # Handle 2FA setup logic
        return Response({'status': '2FA setup complete'}, status=status.HTTP_200_OK)
