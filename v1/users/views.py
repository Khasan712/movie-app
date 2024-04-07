from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import CustomerRegisterSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


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
