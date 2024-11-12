from django.urls import path
from customer import views

urlpatterns = [
    path('', views.SignInView.as_view(), name='signin'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('home/', views.HomePageView.as_view(), name='home'),
    path('product/<int:id>/view/', views.ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:id>/add/cart/', views.AddToCartView.as_view(), name='cart-add'),
    path('user/cart/view/', views.CartView.as_view(), name='cart-view'),
    path('user/cart/product/<int:id>/remove/', views.CartDeleteView.as_view(), name='cart-delete'),
    path('user/cart/product/<int:id>/check-out/', views.CheckOutView.as_view(), name='check-out'),
    path('user/order/view/', views.MyOrderView.as_view(), name='order-view'),
    path('user/order/<int:id>/cancel/', views.CancelOrderView.as_view(), name='order-cancel'),
    path('user/order/<int:id>/return/', views.ReturnOrderView.as_view(), name='order-return'),
    path('offers/products/view/', views.OfferProductView.as_view(), name='offer-product'),
    path('user/order/product/<int:id>/review/', views.ReviewAddView.as_view(), name='add-review'),
    path('user/signout/', views.signout_view, name='signout'),
]
