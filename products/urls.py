from django.urls import path

from products.views import ProductListView, ProductNewView, ProductSaleView, ProductBestView

urlpatterns = [
     path('/', ProductListView.as_view()),
     path('/new', ProductNewView.as_view()),
     path('/sale', ProductSaleView.as_view()),
     path('/best', ProductBestView.as_view()),
]