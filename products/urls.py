from products.views import DetailView
from django.urls import path, include

urlpatterns = [
    path('/<int:pk>', DetailView.as_view()),
]
