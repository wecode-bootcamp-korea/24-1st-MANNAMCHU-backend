from django.urls import path
from django.urls.resolvers import URLPattern
from products.views import ProductListView

urlpatterns = [
    path('product-list', ProductListView.as_view()),
]