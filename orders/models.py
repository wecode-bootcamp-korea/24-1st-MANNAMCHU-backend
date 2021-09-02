from django.db import models

class Order(models.Model):
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE)
    option       = models.ForeignKey('products.Option', on_delete=models.CASCADE)
    address      = models.CharField(max_length=500)
    memo         = models.CharField(max_length=300)
    order_status = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'

class OrderStatus(models.Model):
    status = models.CharField(max_length=100)

    class Meta:
        db_table = 'order_status'

class OrderedItem(models.Model):
    option     = models.ForeignKey('products.Option', on_delete=models.CASCADE)
    quantity    = models.IntegerField()
    order       = models.ForeignKey('Order', on_delete=models.CASCADE)
    item_status = models.ForeignKey('OrderedItemStatus', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'ordered_items'

class OrderedItemStatus(models.Model):
    status = models.CharField(max_length=100)

    class Meta:
        db_table = 'ordered_item_status'

