from django.urls import path

from products.views import ProductListView, DetailView, CartView

urlpatterns = [
     path('/list', ProductListView.as_view()),
     path('/detail', DetailView.as_view()),
     path('/cart', CartView.as_view()),
]
