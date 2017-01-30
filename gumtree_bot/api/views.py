from rest_framework import viewsets

from .serializers import *
from app.models import *



class CategoriesViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriesSerializer

    def get_queryset(self):
        website = self.request.query_params.get('website', None)

        if website and int(website) >0 :
            return Categories.objects.filter(website_id=int(website))

        return Categories.objects.all()