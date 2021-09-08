import json
from django.db.models import expressions

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from users.login_decorator  import login_decorator
from products.models        import Product, Option, Image, ProductTag, Tag, Cart
from users.models           import User

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
    def get(self, request):
        try:
            user  = request.user
            user = User.objects.get(id=1)
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
        
    @login_decorator
    def patch(self, request):
        user = request.user
        try:
            data = json.loads(request.body)

            if not data['quantity']:
                return JsonResponse({"message" : "QUANTITY_ERROR"}, status=400)
            
            Cart.objects.filter(option_id=data['option_id'], user_id=user.id).update(quantity=data['quantity'])
            
            if not Cart.objects.filter(option_id=data['option_id'], user_id=user.id).exists():
                return JsonResponse({"message" : "CART DOES NOT EXISTS"}, status=400)

            return JsonResponse({"message" : "SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"})
    