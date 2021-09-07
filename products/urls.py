from products.views import DetailView
from django.urls import path

from products.views import ProductListView, DetailView

urlpatterns = [
     path('/', ProductListView.as_view()),
     path('/detail', DetailView.as_view()),
]
