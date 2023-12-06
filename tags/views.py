from rest_framework import generics
from .serializers import TagSerializer
from .models import Tag


class TagView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
