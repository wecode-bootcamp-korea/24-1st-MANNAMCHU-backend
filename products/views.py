import json

from django.views import View
from django.http import JsonResponse, HttpResponse
from django.db.utils import DataError
from django.core.paginator import Paginator

from products.models import Product, Option, Image, Tag, Cart


# class ProductListView(View):
#     def get(self, request):
#         product_list = Product.objects.all().order_by('id')
#         paginator = Paginator(product_list, 24)

#         page = request.GET.get('page')
#         posts = paginator.get_page(page) 

#         result = []
    
#         for item in product_list:
#             result.append({
#                 'name'       : item.name,
#                 'price'      : item.price,
#                 'image'      : item.image_set.all(),
#                 'tag'        : item.tag_set.all(),
#                 'like_count' : item.like_count
#             })
#         return JsonResponse({'products': posts})

    
class DetailView(View):
    def get(self, request):
        product_id = request.GET.get('id')
        product_detail = Product.objects.get(id=product_id)

        result = {
            'name'        : product_detail.name,
            'price'       : product_detail.price,
            'like_count'  : product_detail.like_count,
            'description' : product_detail.description,
            'image'       : product_detail.image_set.all(),
            'tag'         : product_detail.tag_set.all()
        }

        return JsonResponse({'product_detail': result})
        

# class CartView(View):
#     def post(self, request):
#         data = json.loads(request.body)
#         input_product = Product.objects.filter(product_id=data['product_id'])

#         try:
#             if not input_product.exists():
#                 return JsonResponse({'message': 'DOES_NOT_EXIST'})
#             product = Product.objects.get(product_id=data['product_id'])
                  
#             Product.objects.create(
#             user = data['user_id'],
#             product_id = data['product_id'],
#             option_id = data['option_id'],
#             quantity = data['quantity']
#         )
#         except KeyError:
#             return JsonResponse({'message': 'KEY_ERROR'})
                

#     def get(self, request):
#         cart_id = request.GET.get('id')
#         cart = Cart.objects.filter(user_id=cart_id)

#         if not cart.exists():
#             return JsonResponse({'message': 'NOTHING_IN_YOUR_CART'})

#         def product_specs(product_id):
#             specs = []
#             product_spec = Product.objects.get(id=product_id)
#             specs.append({
#                 'name': product_spec.id,
#                 'price': product_spec.price,
#                 'image': product_spec.images.url,
#                 'option': product_spec.options.option,
#                 'additional_price': product_spec.options.additional_price
#             })
#             return specs
            
#         result = []
#         for item in cart:
#             result.append({
#                 product_specs(item.id),
#                 'quantity' : item.quantity
#             })
#         return JsonResponse({'result': result}, status=200)

        

#     # def patch(self, request):
        
#     # def delete(delf, request):

    