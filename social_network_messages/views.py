from rest_framework import viewsets, filters

from .models import Message, City
from .serializers import MessageSerializer, CitySerializer


# Create your views here.
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all().order_by('name')
    serializer_class = CitySerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('createdAt')
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'content']
