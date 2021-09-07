from products.views import DetailView,CartView
from django.urls import path

urlpatterns = [
    path('/detail', DetailView.as_view()),
    path('/cart', CartView.as_view()),
]

