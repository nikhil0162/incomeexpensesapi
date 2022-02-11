from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from .models import Expense
from .permissions import *
from .serializers import ExpenseSerializer


class ExpenseListAPIView(ListCreateAPIView):
    queryset = Expense.objects.select_related('owner')
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class ExpenseDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.select_related('owner')
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwner]
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
