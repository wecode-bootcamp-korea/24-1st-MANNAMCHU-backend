from django.db import models

class User(models.Model):
    name     = models.CharField(max_length=45)
    email    = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    phone    = models.CharField(max_length=17)
    address  = models.CharField(max_length=500)

    class Meta:
        db_table = 'users'

class WishList(models.Model):
    user    = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'wishlist'
