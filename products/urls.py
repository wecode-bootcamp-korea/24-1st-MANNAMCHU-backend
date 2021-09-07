from django.urls import path

from products.views import ProductListView, DetailView

urlpatterns = [
     path('/detail', DetailView.as_view()),
     path('/', ProductListView.as_view()),
]