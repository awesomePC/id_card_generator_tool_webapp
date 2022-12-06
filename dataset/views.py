from django.shortcuts import render
from rest_framework import viewsets
from dataset.models import DatasetResource
from dataset.serializers import ViewDatasetSerializer

class ViewDataSet(viewsets.ModelViewSet):
    queryset = DatasetResource.objects.all().order_by('id')
    serializer_class = ViewDatasetSerializer