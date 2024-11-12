from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from customer.forms import SignUpForm, SignInForm, ReviewForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from store.models import Product, Cart, Order, Offer
from django.utils.decorators import method_decorator


def signin_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('signin')
        return func(request, *args, **kwargs)
    return wrapper

def signout_view(request, *args, **kwargs):
    logout(request)
    return redirect('signin')

class SignUpView(View):
    def get(self, request, *args, **kwargs):
        signup_form = SignUpForm()
        return render(request, 'signup.html', {'signup_form':signup_form})
    
    def post(self, request, *args, **kwargs):
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            messages.success(request, 'Registration success')
            return redirect('signin')
        messages.error(request, 'Registration failed')
        return render(request, 'signup.html', {'signup_form':signup_form})

class SignInView(View):
    def get(self, request, *args, **kwargs):
        signin_form = SignInForm()
        return render(request, 'signin.html', {'signin_form':signin_form})
    
    def post(self, request, *args, **kwargs):
        signin_form = SignInForm(request.POST)

        if signin_form.is_valid():
            username = signin_form.cleaned_data.get('username')
            password = signin_form.cleaned_data.get('password')
            user_obj = authenticate(request, username=username, password=password)

            if user_obj:
                login(request, user_obj)
                messages.success(request, 'Login success')
                return redirect('home')
        messages.error(request, 'Login failed')    
        return render(request, 'signin.html', {'signin_form':signin_form})


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        product_objs = Product.objects.all()
        return render(request, 'home.html', {'product_objs':product_objs})

@method_decorator(signin_required, name='dispatch')
class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('id')
        product_obj = Product.objects.get(id=product_id)
        stars = range(1, 6)
        return render(request, 'product-detail.html', {'product_obj':product_obj, 'stars':stars})

@method_decorator(signin_required, name='dispatch')
class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        print(messages)
        quantity = request.POST.get('quantity')
        user = request.user
        product_id = kwargs.get('id')
        product_obj = Product.objects.get(id=product_id)
        cart_objs = Cart.objects.filter(product=product_obj, user=request.user).first()

        if not cart_objs:
            Cart.objects.create(product=product_obj, user=user, quantity=quantity)
            messages.success(request, 'Item added to your cart! View your cart to complete the purchase.')
        else:    
            messages.error(request, 'Item already in your cart')     
        return redirect('home')

@method_decorator(signin_required, name='dispatch')
class CartView(View):
    def get(self, request, *args, **kwargs):
        cart_objs = Cart.objects.filter(user=request.user, status='in-cart')
        return render(request, 'cart-view.html', {'cart_objs':cart_objs})

@method_decorator(signin_required, name='dispatch')
class CartDeleteView(View):
    def get(self, request, *args, **kwargs):
        cart_id = kwargs.get('id')
        Cart.objects.get(id=cart_id).delete()
        messages.success(request, 'Item removed from your cart.')
        return redirect('cart-view')

@method_decorator(signin_required, name='dispatch')
class CheckOutView(View):
    def get(self, request, *args, **kwargs):
        cart_id = kwargs.get('id')
        cart_obj = Cart.objects.get(id=cart_id)
        return render(request, 'check-out.html', {'cart_obj':cart_obj})
    
    def post(self, request, *args, **kwargs):
        cart_id = kwargs.get('id')
        cart_obj = Cart.objects.get(id=cart_id)
        product_obj = cart_obj.product
        address = request.POST.get('address')
        Order.objects.create(product=product_obj, user=request.user, delivery_address=address)
        cart_obj.delete()
        messages.success(request, 'Order placed successfully!')
        return redirect('home')

@method_decorator(signin_required, name='dispatch')
class MyOrderView(View):
    def get(self, request, *args, **kwargs):
        order_objs = Order.objects.filter(user=request.user)
        return render(request, 'order-view.html', {'order_objs':order_objs})

@method_decorator(signin_required, name='dispatch')
class CancelOrderView(View):
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('id')
        order_obj = Order.objects.get(id=order_id)
        order_obj.status = 'cancelled'
        order_obj.save()
        messages.success(request, 'Order cancelled successfully')
        return redirect('home')

@method_decorator(signin_required, name='dispatch')
class ReturnOrderView(View):
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('id')
        order_obj = Order.objects.get(id=order_id)
        order_obj.status = 'returned'
        order_obj.save()
        messages.success(request, 'Return request processing')
        return redirect('home')

@method_decorator(signin_required, name='dispatch')
class ReviewAddView(View):
    def get(self, request, *args, **kwargs):
        review_form = ReviewForm()
        product_id = kwargs.get('id')
        product_obj = Product.objects.get(id=product_id)
        return render(request, 'add-review.html', {'review_form':review_form, 'product_obj':product_obj})
    
    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('id')
        product_obj = Product.objects.get(id=product_id)        
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review_form.instance.user = request.user
            review_form.instance.product = product_obj
            review_form.save()
            messages.success(request, 'Thanks for your review.')
            return redirect('home')
        messages.error(request, 'Failed to add your review.')
        return render(request, 'add-review.html', {'review_form':review_form, 'product_obj':product_obj})

@method_decorator(signin_required, name='dispatch')
class OfferProductView(View):
    def get(self, request, *args, **kwargs):
        offer_objs = Offer.objects.filter(is_active=True)
        return render(request, 'offer-items.html', {'offer_objs':offer_objs})
