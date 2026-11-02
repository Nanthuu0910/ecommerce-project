from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('',home,name='home'),
    path('search/',search,name='search'),
    path('register/',register,name='register'),
    path('login/',user_login,name='login'),
    path('user_dashboard/',user_dashboard,name='user_dashboard' ),
    path('become_seller/',become_seller,name='become_seller'),
    path('seller/',seller_dashboard,name='seller_dashboard'),
    path('products/',products,name='products'),
    path('admin_dashboard/',admin_dashboard,name='admin_dashboard'),
    path('admin_accept/<int:id>/',admin_accept,name='admin_accept'),
    # path('admin_reject/<int:id>/',admin_reject,name='admin'),
    path('status_info/',status_info,name='status_info'),
    path('logout/',user_logout,name='logout'),
    path('category/<str:category>',category,name='category'),
    path('add_product/', add_product, name='add_product'),
    path('product/<int:product_id>/',product_detail,name='product_detail'),
    path('update_product/<int:id>', update_product, name='update_product'),
    path('delete_products/<int:id>', delete_product, name='delete_product'),
    path('wishlist/<int:id>',wishlist,name='wishlist'),
    path('wishlist/',allwishlist,name='allwishlist'),
    path('add_to_cart/<int:id>',add_to_cart,name='add_to_cart'),
    path('cart/',cart,name='cart'),
    path('remove_cart/<int:id>',remove_cart,name='remove_cart'),
    path('quantity_change/<int:id>',quantity_change,name='quantity_change'),
    path('order/',buy,name='order'),
    path('orderdetails_seller/',orderdetails_seller,name='orderdetails_seller'),
    
    
    

   

]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)