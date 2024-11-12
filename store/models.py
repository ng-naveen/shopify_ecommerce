from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


def get_expected_delivery_date():
    return datetime.date.today() + datetime.timedelta(days=10)

class Category(models.Model):
    category_name = models.CharField(max_length=250, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name
    

class Product(models.Model):
    product_name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name

    @property
    def get_offer_price(self):
        offer_obj = Offer.objects.filter(product=self, is_active=True).first()
        if offer_obj:
            offer_price = self.price - offer_obj.discount
            return offer_price
        
    @property    
    def get_reviews(self):
        review_objs = Review.objects.filter(product=self)
        return review_objs
    
    @property
    def get_avg_rating(self):
        review_objs = self.get_reviews
        if review_objs:
            avg_rating = sum([review_obj.rating for review_obj in review_objs]) // 2
            return avg_rating
        return 0
    

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=250, default='in-cart')


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=250)
    ordered_date = models.DateField(auto_now_add=True)
    expected_delivery_date = models.DateField(default=get_expected_delivery_date)
    order_options = (
        ('order-placed', 'order-placed'),
        ('shipped', 'shipped'),
        ('in-transit', 'in-transit'),
        ('delivered', 'delivered'),
        ('returned', 'returned'),
        ('cancelled', 'cancelled'),
    )
    status = models.CharField(max_length=250, choices=order_options, default='order-placed')


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.CharField(max_length=250)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])


class Offer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
