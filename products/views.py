from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from products.models import Product


class DetailView(View):
    def get(self, request):
        def getting_images():
            image_list = product_detail.image_set.filter(product_id=product_detail.id).values('id', 'url')
            image_set  = []

            image_set.append([({
                'id' : image['id'],
                'url': image['url']}) for image in image_list])
            return image_set
        
        def getting_options():
            option_list = product_detail.option_set.filter(product_id=product_detail.id).values('id', 'option', 'additional_price')
            option_set  = []

            option_set.append([({
                'id'              : option['id'],
                'option'          : option['option'],
                'additional_price': option['additional_price']}) for option in option_list])
            return option_set

        try:
            product_id     = request.GET.get('id')
            product_detail = Product.objects.get(id=product_id)

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
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'PAGE_NOT_FOUND'}, status=404)
            