import json

from django.views          import View
from django.http           import JsonResponse
from django.core.paginator import Paginator

from users.login_decorator import login_decorator
from products.models       import Product, Image, ProductTag, Tag, Cart

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

class CartView(View):
    @login_decorator
    def get(self, request):
        user = request.user
        carts = Cart.objects.filter(user_id=user.id)

        result = [{
            'product'  : cart.option.product.name,
            'price' : cart.option.product.price,
            'option': cart.option.option,
            'addtional_price' : cart.option.addtional_price,
            'quantity' : cart.quantity,
            'image' : cart.option.product.image_set.values('url'),
            'sale_rate' : cart.option.product.producttag_set.values('sale_rate'),
        }for cart in carts]
        return JsonResponse({"message" : result}, status=200)

    @login_decorator
    def patch(self, request):
        user = request.user
        data = json.loads(request.body)

        cart = Cart.objects.get
        return JsonResponse({"message" : "SUCCESS"}, status=200)

