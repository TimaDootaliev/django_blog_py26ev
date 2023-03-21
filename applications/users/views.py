from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import RegistrationSerializer, ActivationSerializer, LoginSerializer


class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'message': 'Thanks for registration!'})
    

class ActivationView(CreateAPIView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = ActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.activate()
        return Response({'message': 'Аккаунт успешно активирован!'})


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer