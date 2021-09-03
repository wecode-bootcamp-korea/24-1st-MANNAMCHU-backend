from django.db import models

class Product(models.Model):
    name        = models.CharField(max_length=100)
    price       = models.DecimalField(max_digits=18, decimal_places=2)
    like_count  = models.IntegerField(blank=True, default=0)
    description = models.TextField()
    origin      = models.CharField(max_length=500)
    tags        = models.ManyToManyField('Tag', through='ProductTag')

    class Meta:
        db_table = 'products'

class Option(models.Model):
    option           = models.CharField(max_length=100)
    additional_price = models.DecimalField(max_digits=18, decimal_places=2, blank=True, default=0)
    product          = models.ForeignKey('Product', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'options'

class Image(models.Model):
    url     = models.URLField(max_length=1000)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'images'

class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'tags'

class ProductTag(models.Model):
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)
    tag       = models.ForeignKey('Tag', on_delete=models.CASCADE)
    sale_rate = models.IntegerField(blank=True, default=0)
    
    class Meta:
        db_table = 'product_tags'

class Cart(models.Model):
    user     = models.ForeignKey('users.User', on_delete=models.CASCADE)
    option   = models.ForeignKey('products.Option', on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, default=0)

    class Meta:
        db_table = 'carts'
