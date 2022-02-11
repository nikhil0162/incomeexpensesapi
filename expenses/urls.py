from django.urls import path

from .views import *

app_name= 'expenses'

urlpatterns = [
    path('', ExpenseListAPIView.as_view(), name="expenses-list"),
    path('<int:id>/', ExpenseDetailAPIView.as_view(), name="expenses-detail"),
]
