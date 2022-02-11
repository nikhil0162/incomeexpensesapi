from django.urls import path

from .views import *

app_name= 'income'

urlpatterns = [
    path('', IncomeListAPIView.as_view(), name="income-list"),
    path('<int:id>/', IncomeDetailAPIView.as_view(), name="income-detail"),
]
