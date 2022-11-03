import secrets
from django.db import models

from . paystack import PayStack
from users.models import Customer
# Create your models here.
class Banner(models.Model):
    banner = models.ImageField(upload_to='banner')
    create = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{str(self.create)}'

    
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    passenger = models.PositiveIntegerField()
    luggages = models.PositiveIntegerField()
    transmission = models.CharField(max_length=255)
    doors = models.PositiveIntegerField()
    refueling = models.TextField()
    washing = models.TextField()
    smoking = models.TextField()
    included = models.CharField(max_length=255)
    excluded = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product')
    image1 = models.ImageField(upload_to='product')
    image2 = models.ImageField(upload_to='product')
    image3 = models.ImageField(upload_to='product')
    stars = models.PositiveIntegerField()
    create = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null = True, blank=True)
    total = models.PositiveIntegerField()
    create = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Cart :::: {str(self.id)}'


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE , null=True, blank=True)
    quantity = models.PositiveIntegerField()
    rate = models.PositiveIntegerField()
    subtotal= models.PositiveIntegerField()
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'cart::: {str(self.cart.id)}'


ORDER_STATUS=(
    ('Order Received','Order Received'),
    ('Order Processing','Order Processing'),
    ('Order Cancelled','Order Cancelled'),
    ('Order Completed','Order Completed'),
)
PAYMENT_METHOD=(
    ('Transfer','Transfer'),
    ('Paystack','Paystack'),
)
class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE,null =True, blank =True)
    ordered_by = models.CharField(max_length=255)
    shipping_address = models.CharField(max_length=255)
    phone = models.CharField(max_length=14)
    email = models.CharField(max_length=255)
    order_status = models.CharField(max_length=255, choices=ORDER_STATUS, default='Order Received')
    discount = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    create = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=255, choices=PAYMENT_METHOD, default='Paystack')
    payment_completed = models.BooleanField(default=False,null =True, blank =True)
    ref = models.CharField(max_length=255,null =True, blank =True)
    
    def __str__(self):
        return f'{self.order_status} ::: {str(self.id)}'

    # ref code
    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            obj_with_sm_ref = Order.objects.filter(ref = ref)
            if not obj_with_sm_ref:
                self.ref = ref
        super().save(*args,**kwargs)

    
    # amount
    def amount_value(self)->int:
        return self.amount * 100

    # verify payment
    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount']/100 == self.amount:
                self.payment_completed = True
            self.save()

        if self.order_status == 'Order Completed':
            self.save()
            self.cart.delete()
        if self.payment_completed:
            return True
        return False
