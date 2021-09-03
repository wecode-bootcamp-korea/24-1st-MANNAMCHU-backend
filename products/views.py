import json

from django.views import View
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db.utils import DataError

from products.models import Product, Option, Image, Tag, Cart


class DetailView(View):
    def get(self, request):
        product_id     = request.GET.get('product-id')
        product_detail = Product.objects.get(id=product_id)

        def getting_images():
            image_list = product_detail.image_set.filter(product_id=product_detail.id).values('id', 'url')
            image_set  = []
            for image in image_list:
                image_set.append({
                    'id' : image['id'],
                    'url': image['url']
                })
            return image_set
        
        def getting_options():
            option_list = product_detail.option_set.filter(product_id=product_detail.id).values('id', 'option', 'additional_price')
            option_set  = []
            for option in option_list:
                option_set.append({
                    'id'              : option['id'],
                    'option'          : option['option'],
                    'additional_price': option['additional_price']
                })
            return option_set

        result = {
            'name'        : product_detail.name,
            'price'       : product_detail.price,
            'like_count'  : product_detail.like_count,
            'description' : product_detail.description,
            'options'     : getting_options(),
            'origin'      : product_detail.origin,
            'image'       : getting_images(),
            'tag'         : [{
                    'new' : product_detail.tag.new,
                    'sale': product_detail.tag.sale,
                    'best': product_detail.tag.best
            }]
        }
        return JsonResponse({'product_detail': result})
        