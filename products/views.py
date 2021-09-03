from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator


from products.models import Product


class ProductListView(View):
    def get(self, request):
        try:
            page     = request.GET.get('page')
            products = Product.objects.all().order_by('id')
            result   = []
                
            for product in products:
                result.append({
                    'name'       : product.name,
                    'price'      : product.price,
                    'discount'   : product.discount,
                    'image'      : list(product.image_set.filter(product_id=product.id).values('url')),
                    'tag'        : [{
                        'new'        : product.tag.new,
                        'sale'       : product.tag.sale,
                        'best'       : product.tag.best
                    }],
                    'like_count' : product.like_count
                })
            
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
            products = Product.objects.all()
            result   = []
            for product in products:
                if product.tag.new:
                    result.append({
                        'name'       : product.name,
                        'price'      : product.price,
                        'discount'   : product.discount,
                        'image'      : list(product.image_set.filter(product_id=product.id).values('url')),
                        'tag'        : [{
                            'new'        : product.tag.new,
                            'sale'       : product.tag.sale,
                            'best'       : product.tag.best,
                        }],
                        'like_count' : product.like_count
                    })
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
            products = Product.objects.all()
            result   = []
            for product in products:
                if product.tag.best:
                    result.append({
                        'name'       : product.name,
                        'price'      : product.price,
                        'discount'   : product.discount,
                        'image'      : list(product.image_set.filter(product_id=product.id).values('url')),
                        'tag'        : [{
                            'new'        : product.tag.new,
                            'sale'       : product.tag.sale,
                            'best'       : product.tag.best,
                        }],
                        'like_count' : product.like_count
                    })
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
            result   = []
            for product in products:
                if product.tag.sale:
                    result.append({
                        'name'       : product.name,
                        'price'      : product.price,
                        'discount'   : product.discount,
                        'image'      : list(product.image_set.filter(product_id=product.id).values('url')),
                        'tag'        : [{
                            'new'        : product.tag.new,
                            'sale'       : product.tag.sale,
                            'best'       : product.tag.best,
                        }],
                        'like_count' : product.like_count
                    })
            paginator = Paginator(result, 24)

            if paginator.num_pages < int(page):
                return JsonResponse({"message" : "OUT OF RANGE"}, status=404)

            posts = paginator.get_page(page)

            return JsonResponse({"sale_products" : posts.object_list}, status=200)
        except ValueError:
            return JsonResponse({"message" : "PAGE NOT FOUND"}, status=404)

            