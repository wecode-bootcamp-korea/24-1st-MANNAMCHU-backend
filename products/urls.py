from products.views import DetailView
from django.urls import path

urlpatterns = [
    path('/', DetailView.as_view()),
    path('/detail', DetailView.as_view()),
