from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('',home,name='home'),
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
   

]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)