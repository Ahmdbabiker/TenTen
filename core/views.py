from django.shortcuts import render , redirect
from .models import * 
from django.contrib import messages
from django.db.models import Avg
from order.models import *
from django.db.models import Sum
from django.utils import timezone
import time
from datetime import timedelta
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.http import StreamingHttpResponse
import json



# Create your views here.

def home(request):
    all_products = Product.objects.all()
    best_seller = Product.objects.order_by('-no_of_buying')[:3]
    data = {"all_products":all_products , 
    "best":best_seller}
    return render(request , "index.html" , data)

def meal_details(request , slug_name):
    get_meal = Product.objects.get(slug = slug_name)
    similar = Product.objects.filter(tag = get_meal.tag ).exclude(slug = slug_name)
    all_products = Product.objects.all()
    for product in all_products:
        ratings = product.product_rate()
        rates = [rating.rate for rating in ratings]
    
    if request.POST:
        rate = request.POST.get("rate")
        comment = request.POST.get("comment")
        user = request.user
        if user.is_authenticated:
            if Rating.objects.filter(user_rated = user , product__slug = slug_name).exists():
                messages.error(request , "لقد قمت بالتعليق بالفعل على هذا العنصر")
                return redirect("meal_detail" , slug_name)
            else:
                Rating.objects.create(
                    product = get_meal , user_rated = user , 
                    comment = comment , rate = rate)
                messages.success(request , "شكراً لك على تقييمك ")
        else:
            messages.error(request , "قم بإنشاء حساب لترك تقييم ")
    meal_Rate = Rating.objects.filter(product__slug = get_meal.slug)
    meal_avg = meal_Rate.aggregate(Avg('rate'))
    avg_extracted = meal_avg['rate__avg']
    count_rating = meal_Rate.count()
    

    data = {"meal_details":get_meal ,
    "similar":similar , "rate":meal_Rate , 
    "avg_rate" : avg_extracted ,"rates":rates, "count_rating":count_rating}
    return render(request , "meal_details.html" , data)

def admindash(request):
    if request.user.is_superuser:
        products = Product.objects.all().count()
        rate = Rating.objects.all()
        rate_Avg = rate.aggregate(Avg('rate'))
        rate_extrcated = rate_Avg['rate__avg']
        orders = Order.objects.all().count()
        users = User.objects.all().exclude(is_superuser = True).count()
        best_seller = Product.objects.order_by("-no_of_buying").first()
        total = Order.objects.aggregate(total_paid=Sum('amount_paid'))['total_paid'] or 0 
        total_formatted = f"{total:.2f}" 
        data = {"products":products , "rate":rate_extrcated , 
        "orders":orders , "users":users , "best_seller":best_seller , 
        "total":total_formatted}
    else:
        messages.error(request, "دخول خاطئ")
        return redirect("home")
    return render(request , "admin_page.html" , data)


def admin_orders(request , order_type):
    if request.user.is_superuser : 
        today = timezone.now().date()
        order_no = order_type
        orders = None
        order_items = None
        if order_type == 1:
            orders = Order.objects.all()
            paginator = Paginator(orders , 10)
            page_number = request.GET.get('page')  
            orders = paginator.get_page(page_number) 

            for order in orders :
                order_items = order.orderitem_set.all()

        elif order_type == 2 :
           print("live orders")
        elif order_type ==3 : 
            orders = Order.objects.filter(date_ordered__date = today)
            orders = Order.objects.all()
            paginator = Paginator(orders , 10)
            page_number = request.GET.get('page')  
            orders = paginator.get_page(page_number) 
            print(orders)
        elif order_type == 4 :
            orders = Order.objects.filter(user__is_superuser = True)
        elif order_type == 5 :
            orders = Order.objects.filter(user__is_superuser = False)
        elif order_type == 6 :
            last_7 = today - timedelta(days=7)
            orders = Order.objects.filter(date_ordered__date__gte = last_7)
            orders = Order.objects.all()
            paginator = Paginator(orders , 10)
            page_number = request.GET.get('page')  
            orders = paginator.get_page(page_number) 
            print(orders)
        elif  order_type == 7 :
            last_30 = today - timedelta(days=30)
            orders = Order.objects.filter(date_ordered__date__gte = last_30)
            orders = Order.objects.all()
            paginator = Paginator(orders , 10)
            page_number = request.GET.get('page')  
            orders = paginator.get_page(page_number) 
            print(orders)
        data = {"orders":orders , 
        "order_no":order_no , "order_items":order_items}
        return render(request , "admin_orders.html" , data )
    else:
        messages.success(request , "دخول خاطىء")
        return redirect("home")


def general_rating(request , rate_int):
    rate = Rating.objects.all()
    rate_Avg = rate.aggregate(Avg('rate'))
    rate_extrcated = rate_Avg['rate__avg']   
    rate_score = None
    rate_int = int(rate_int)

    if rate_int == 0:
        rate_score = Rating.objects.all()  
    elif 1 <= int(rate_int) <= 5:
        rate_score = Rating.objects.filter(rate=rate_int)  

    data = {"rate_extrcated":rate_extrcated , "rate_score":rate_score} 
    return render(request , "gen_rate.html" ,data)

def get_new_orders(request):
    if request.method == "GET":
        new_orders = Order.objects.filter(is_new=True)
        orders_data = [{'id': order.id} for order in new_orders]
        return JsonResponse({'orders': orders_data})

def order_detail(request , order_id):
    order_item = OrderItem.objects.filter(order__id = order_id)
    order = Order.objects.get(id = order_id)
    order.is_new = False
    order.save()
    data = {"order_item":order_item , "order":order}
    return render(request , "order_detail.html" , data)

def product_admin(request):
    all_products = Product.objects.all()
    if request.method == 'POST':
        product_id = request.POST.get("product")
        get_product = Product.objects.get(id = product_id)
        get_product.delete()
        return redirect("product_admin")
    data = {"all_products":all_products}
    return render(request , "manage_product.html" ,data)

def edit_product(request , product_id):
    get_product = Product.objects.get(id = product_id)
    if request.method == "POST":
        name = request.POST.get("name")
        desc = request.POST.get("desc")
        price = request.POST.get("price")
        image = request.FILES.get("image")

        get_product.name = name
        get_product.desc = desc
        get_product.price = price
        
        if image:
            get_product.image = image

        get_product.save()

        messages.success(request , "تم التعديل")
        return redirect("product_admin")

    
    data = {"get_product":get_product}
    return render(request , "edit_product.html" , data)

def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        desc = request.POST.get("desc")
        price = request.POST.get("price")
        image = request.FILES.get("image")
        tag = request.POST.get("tag")
        slug = slugify(name)
        
        tag_selected = None

        if tag == '1' :
            tag_selected = Tag.objects.get(id = 1 )
        elif tag == '2' :
            tag_selected = Tag.objects.get(id = 2 )
        elif tag == '3' :
            tag_selected = Tag.objects.get(id = 3 )


        add_new_product = Product.objects.create(name = name , slug =slug, desc = desc , 
        price = price , image = image ,tag = tag_selected)
        add_new_product.save()
        messages.success(request , "تمت الإضافة")
        return redirect("product_admin")

    return render(request , "add_product.html" )

def user_orders(request , user_id):
    current_user = request.user.id
    get_user = OrderItem.objects.filter(user__id = current_user)
    data  = {"user_orders":get_user}
    return render(request, "my_orders.html" , data)

def order_done(request):
    get_session = request.session.get("order_no")
    data = {"order_id":get_session}
    return render(request , "order_done.html" , data)

def edit_shiping_phone(request , user_id):
    current_user = request.user.id
    grap_user = Profile.objects.get(user__id = current_user)
    if request.method == "POST":
        phoneno = request.POST.get("phoneno")
        address = request.POST.get("address")

        grap_user.phone_number = phoneno
        grap_user.address = address
        grap_user.save()
        messages.success(request , "تم تعديل البيانات")
        return redirect("home")
    data = {"grap_user":grap_user}
    return render(request , 'edit_ship_details.html' , data)