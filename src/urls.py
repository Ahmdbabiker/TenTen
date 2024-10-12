from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , home , name='home'),
    path('meal_detials/<slug:slug_name>' ,meal_details , name="meal_detail"),
    path('accounts/' , include('accounts.urls')),
    path('cart/' , include('cart.urls')),
    path('order/' , include('order.urls')),
    path('admin_dashboard' , admindash , name="admindash"),
    path('admin_orders/<int:order_type>' , admin_orders , name="admin_orders"),
    path('get-new-orders/', get_new_orders, name='get_new_orders'),
    path('order_detail/<int:order_id>/' , order_detail , name="order_detail"),
    path('general_rate/<int:rate_int>' , general_rating , name="general_rating"),
    path('manage_products' , product_admin , name="product_admin"),
    path('manage_products/edit/<int:product_id>' , edit_product , name="edit_product"),
    path('manage_products/add_product' , add_product , name="add_product"),
    path('myorders/<int:user_id>' , user_orders , name="myorders"),
    path('orderDone' , order_done , name="order_done"),
    path('edit_shipping_phone_number/<int:user_id>' , edit_shiping_phone , name="edit_shiping_phone"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

