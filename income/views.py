from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from .models import Income
from .permissions import *
from .serializers import IncomeSerializer


class IncomeListAPIView(ListCreateAPIView):
    queryset = Income.objects.select_related('owner')
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class IncomeDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.select_related('owner')
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwner]
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
