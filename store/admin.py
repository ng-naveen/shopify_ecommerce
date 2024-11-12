from django.contrib import admin
from store.models import Category, Product, Cart, Order, Review, Offer

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(Offer)

