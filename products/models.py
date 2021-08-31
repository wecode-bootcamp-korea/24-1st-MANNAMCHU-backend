from django.db import models
from users import models

class Product(models.Model):
    name        = models.CharField(max_length=100)
    price       = models.DecimalField(max_digits=18, decimal_places=2)
    like_count  = models.IntegerField()
    description = models.TextField()
    image       = models.ForeignKey('Image', on_delete=models.CASCADE)
    tag         = models.ForeignKey('Tag', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'

class Option(models.Model):
    option           = models.CharField(max_length=100)
    additional_price = models.DecimalField(max_digits=18, decimal_places=2)
    quantity         = models.IntegerField()
    product          = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'options'

class Image(models.Model):
    url = models.URLField(max_length=1000)

    class Meta:
        db_table = 'urls'

class Tag(models.Model):
    tag_new  = models.BooleanField()
    tag_sale = models.BooleanField()
    tag_best = models.BooleanField()

    class Meta:
        db_talbe = 'tags'

class Cart(models.Model):
    user    = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    option  = models.ForeignKey('Option', on_delete=models.CASCADE)

    class Meta:
        db_table = 'carts'