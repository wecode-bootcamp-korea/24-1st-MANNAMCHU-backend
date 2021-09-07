import json

from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import DataError

from products.models import Product, Option, Image, ProductTag, Tag, Cart
from users.models import User


class DetailView(View):
    def get(self, request):
        try:
            product_id     = request.GET.get('id')
            product_detail = Product.objects.get(id=product_id)

            image_list  = Image.objects.filter(product_id=product_id).values('id', 'url')
            option_list = Option.objects.filter(product_id=product_id).values('id', 'option', 'additional_price')
            tag_list    = ProductTag.objects.filter(product_id=product_id).values('product_id','sale_rate', 'tag_id')

            result = {
                'name'        : product_detail.name,
                'price'       : product_detail.price,
                'like_count'  : product_detail.like_count,
                'description' : product_detail.description,
                'origin'      : product_detail.origin,
                'options'     : [({
                    'id'               : option['id'],
                    'option'           : option['option'],
                    'additional_price' : option['additional_price']}) for option in option_list],
                'image'       : [({
                    'id' : image['id'],
                    'url': image['url']}) for image in image_list],
                'tag' : [({
                    'product_id' : tag['product_id'],
                    'sale_rate'  : tag['sale_rate'],
                    'tag_id'     : Tag.objects.get(id=tag['tag_id']).name}) for tag in tag_list],
            }
            return JsonResponse({'product_detail': result})
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'PRODUCT_NOT_EXIST'}, status=404)
            

class CartView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            if not User.objects.filter(id=data['user_id']).exists():
                return JsonResponse({'message': 'INVALID_USER'}, status=401)
            if not Option.objects.filter(id=data['option_id']).exists():
                return JsonResponse({'message': 'INVALID_OPTION'}, status=400)

            if Cart.objects.filter(user_id=data['user_id'], option_id=data['option_id']).exists():
                option = Cart.objects.get(option_id=data['option_id'])
                option.quantity += int(data['quantity'])
                option.save()
                return JsonResponse({'message': 'ALREADY_IN_YOUR_CART, MORE_ADDED'}, status=201)

            Cart.objects.create(
                user_id   = data['user_id'],
                option_id = data['option_id'],
                quantity  = data['quantity'])
            return JsonResponse({'message': 'ADDED_ITEM_INTO_YOUR_CART'}, status=201)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status=400)
        except DataError:
            return JsonResponse({'message': 'TOO_BIG_NUMBER'}, status=400)

    def delete(self, request):
        product_id = request.GET.get('option_id')

        try:
            target_item = Cart.objects.get(option_id=product_id)
            target_item.delete()
            return JsonResponse({'message': 'ITEM_DELETED'}, status=200)
        
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'ITEM_DOES_NOT_EXIST'}, status=400)

