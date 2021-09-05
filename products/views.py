from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator

from products.models import Product, Image, ProductTag, Tag

class ProductListView(View):
    def get(self, request):
        try:
            page     = request.GET.get('page')
            products = Product.objects.all().order_by('-id')
            sale     = Tag.objects.get(name='sale')
            result   = [{
                    'name'       : product.name,
                    'price'      : product.price,
                    'discount'   : ProductTag.objects.get(product_id=product.id, tag_id=sale.id).sale_rate,
                    'image'      : Image.objects.filter(product_id=product.id).values('url'),
                    'tag'        : product.tags.values('name'),
                    'like_count' : product.like_count
                } for product in products]

            paginator = Paginator(result, 24)
            
            if paginator.num_pages < int(page):
                return JsonResponse({"message" : "OUT OF RANGE"}, status=404)

            posts     = paginator.get_page(page)

            return JsonResponse({'products': posts.object_list}, status=200)
        except ValueError:
            return JsonResponse({"message" : "PAGE NOT FOUND"}, status=404)

class ProductNewView(View):
    def get(self, request):
        try:
            page     = request.GET.get('page')        
            products = Product.objects.all().order_by('-id')
            sale     = Tag.objects.get(name='sale')
            new      = Tag.objects.get(name='new')

            result   = [{
                        'name'       : product.name,
                        'price'      : product.price,
                        'discount'   : ProductTag.objects.get(product_id=product.id, tag_id=sale.id).sale_rate,
                        'image'      : Image.objects.filter(product_id=product.id).values('url'),
                        'tag'        : list(product.tag.value('name')),
                        'like_count' : product.like_count
                    } for product in products if ProductTag.objects.filter(product_id=product.id, tag_id=new.id).exists()]

            paginator = Paginator(result, 24)

            if paginator.num_pages < int(page):
                return JsonResponse({"message" : "OUT OF RANGE"}, status=404)

            posts = paginator.get_page(page)

            return JsonResponse({"new_products" : posts.object_list}, status=200)
        except ValueError:
            return JsonResponse({"message" : "PAGE NOT FOUND"}, status=404)


class ProductBestView(View):
    def get(self, request):
        try:
            page     = request.GET.get('page')
            products = Product.objects.all().order_by('-id')
            sale     = Tag.objects.get(name='sale')
            best     = Tag.objects.get(name='best')

            result   = [{
                        'name'       : product.name,
                        'price'      : product.price,
                        'discount'   : ProductTag.objects.get(product_id=product.id, tag_id=sale.id).sale_rate,
                        'image'      : Image.objects.filter(product_id=product.id).values('url'),
                        'tag'        : list(product.tag.value('name')),
                        'like_count' : product.like_count
                    } for product in products if ProductTag.objects.filter(product_id=product.id, tag_id=best.id).exists()]
            
            paginator = Paginator(result, 24)

            if paginator.num_pages < int(page):
                return JsonResponse({"message" : "OUT OF RANGE"}, status=404)

            posts = paginator.get_page(page)

            return JsonResponse({"best_products" : posts.object_list}, status=200)
        except ValueError:
            return JsonResponse({"message" : "PAGE NOT FOUND"}, status=404)

class ProductSaleView(View):
    def get(self, request):
        try:
            page     = request.GET.get('page')
            products = Product.objects.all()
            sale     = Tag.objects.get(name='sale')
            
            result   = [{
                        'name'       : product.name,
                        'price'      : product.price,
                        'discount'   : ProductTag.objects.get(product_id=product.id, tag_id=sale.id).sale_rate,
                        'image'      : Image.objects.filter(product_id=product.id).values('url'),
                        'tag'        : list(product.tag.value('name')),
                        'like_count' : product.like_count
                    } for product in products if ProductTag.objects.filter(product_id=product.id, tag_id=sale.id).exists()]

            paginator = Paginator(result, 24)

            if paginator.num_pages < int(page):
                return JsonResponse({"message" : "OUT OF RANGE"}, status=404)

            posts = paginator.get_page(page)

            return JsonResponse({"sale_products" : posts.object_list}, status=200)
        except ValueError:
            return JsonResponse({"message" : "PAGE NOT FOUND"}, status=404)
