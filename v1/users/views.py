from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import CustomerRegisterSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class MeApiV1(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'phone': user.phone_number,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
        })


class CustomLoginApiV1(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'role': user.role
        })


class CustomerRegisterApiV1(CreateAPIView):
    queryset = User
    serializer_class = CustomerRegisterSerializer
