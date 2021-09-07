from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from products.models import Product, Option, Image, ProductTag, Tag


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
            