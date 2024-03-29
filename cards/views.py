from rest_framework import generics
from .models import Card
from .serializers import CardSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from transactions.permissions import IsOwnerOrSuperUser


class CardView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrSuperUser]

    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Card.objects.all()
        else:
            return Card.objects.filter(user=user, is_active=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CardDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrSuperUser]

    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def perform_destroy(self, instance: Card):
        instance.is_active = False
        instance.save()
