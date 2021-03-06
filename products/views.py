import json

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import DataError

from users.login_decorator  import login_decorator
from products.models        import Product, Option, Image, ProductTag, Tag, Cart


class ProductListView(View):
    def get(self, request):
        page       = request.GET.get('page', 1)
        tag        = request.GET.get('tag')
        page       = int(page or 1)
        page_size  = 24
        limit      = page_size * page 
        offset     = limit - page_size
        sale       = Tag.objects.get(name='sale')
        try:
            if not tag:
                products   = Product.objects.all().order_by('-id') [offset:limit]
            else:
                tag_object = Tag.objects.get(name=tag)
                products   = Product.objects.filter(tags=tag_object.id).order_by('-id') [offset:limit]
            
            if not products:
                return JsonResponse({"message" : "PAGE NOT FOUND"}, status=404)
            
            result   = [{
                    'id'         : product.id,
                    'name'       : product.name,
                    'price'      : product.price,
                    'discount'   : [discount.sale_rate for discount in ProductTag.objects.filter(product_id=product.id, tag_id=sale.id)], 
                    'image'      : [url.url for url in Image.objects.filter(product_id=product.id)],                           
                    'tag'        : [tag.name for tag in product.tags.all()],
                    'like_count' : product.like_count
                } for product in products]
            return JsonResponse({'products': result, 'page' : page }, status=200)
        except Product.DoesNotExist:
            return JsonResponse({"message" : "DATA NOT FOUND"}, status=400)
        except Tag.DoesNotExist:
            return JsonResponse({"message" : "TAG DOES NOT EXISTS"}, status=400)

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
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        user = request.user
        
        try:
            for datum in data:
                obj, created = Cart.objects.update_or_create(
                    user_id   = user.id,
                    option_id = datum['option_id'],
                    defaults={'quantity': datum['quantity']}
                    )
            return JsonResponse({'message': 'ADDED_ITEM_INTO_YOUR_CART'},  status=201)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status=400)
        except DataError:
            return JsonResponse({'message': 'TOO_BIG_NUMBER'}, status=400)
            
    @login_decorator
    def delete(self, request):
        product_id = request.GET.get('option_id')

        try:
            target_item = Cart.objects.get(option_id=product_id)
            target_item.delete()
            return JsonResponse({'message': 'ITEM_DELETED'}, status=200)
        
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'ITEM_DOES_NOT_EXIST'}, status=400)

    @login_decorator
    def get(self, request):
        try:
            user  = request.user
            
            if not Cart.objects.filter(user_id=user.id).exists():
                return JsonResponse({"message" : "CART EMPTY"}, status=200)

            carts = Cart.objects.filter(user_id=user.id)
            sale  = Tag.objects.get(name='sale')

            result = [{
                'product'         : cart.option.product.name,
                'price'           : cart.option.product.price,
                'option_id'       : cart.option.id,
                'option'          : cart.option.option,
                'addtional_price' : cart.option.additional_price,
                'quantity'        : cart.quantity,
                'image'           : Image.objects.filter(product_id = cart.option.product.id).first().url,
                'sale_rate'       : [discount.sale_rate for discount in ProductTag.objects.filter(product_id=cart.option.product.id, tag_id=sale.id)],
            }for cart in carts]
            
            return JsonResponse({"message" : result}, status=200)
        except Cart.DoesNotExist:
            return JsonResponse({"message" : "CART_DATA_ERROR"}, status=400)
        except Tag.DoesNotExist:
            return JsonResponse({"message" : "TAG_DATA_ERROR"}, status=400)
        except Option.DoesNotExist:
            return JsonResponse({"message" : "OPTION_DATA_ERROR"}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({"message" : "PRODUCT_DATA_ERROR"}, status=400)            
        
