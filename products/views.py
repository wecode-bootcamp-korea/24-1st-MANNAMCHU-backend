from django.views          import View
from django.http           import JsonResponse
from django.core.paginator import Paginator

from users.login_decorator import login_decorator
from products.models       import Product, Image, ProductTag, Tag, Cart

class ProductListView(View):
    def get(self, request):
        try:
            page      = request.GET.get('page', 1)
            tag       = request.GET.get('tag')
            page      = int(page or 1)
            page_size = 1
            limit     = page_size * page 
            offset    = limit - page_size
            
            sale     = Tag.objects.get(name='sale')
            best     = Tag.objects.get(name='best')
            new      = Tag.objects.get(name='new')

            if not tag:
                products = Product.objects.all().order_by('-id') [offset:limit]
        
            elif str(tag) =='sale':
                products = Product.objects.filter(tags=sale.id).order_by('-id') [offset:limit]
            elif str(tag) =='new':
                products = Product.objects.filter(tags=new.id).order_by('-id') [offset:limit]
            elif str(tag) =='best':
                products = Product.objects.filter(tags=best.id).order_by('-id') [offset:limit]

            if not products:
                return JsonResponse({"message" : "PAGE NOT FOUND"}, status=404)
                    
            result   = [{
                    'name'       : product.name,
                    'price'      : product.price,
                    'discount'   : list(ProductTag.objects.filter(product_id=product.id, tag_id=sale.id).values('sale_rate')), # 문제 : 
                    'image'      : list(Image.objects.filter(product_id=product.id).values('url')),
                    'tag'        : list(product.tags.values('name')),
                    'like_count' : product.like_count
                } for product in products]
            return JsonResponse({'products': result, 'page' : page }, status=200)
        except Product.DoesNotExist:
            return JsonResponse({"message" : "DATA NOT FOUND"}, status=400)
        except UnboundLocalError:
            return JsonResponse({"message" : "TAG DOES NOT EXISTS"}, status=400)
