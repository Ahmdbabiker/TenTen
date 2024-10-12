from django.shortcuts import render , redirect
from django.contrib.auth import authenticate  , login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from core.models import Profile
# Create your views here.


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "الرجاء إدخال اسم المستخدم وكلمة المرور")
            return render(request, "loginn.html")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "تم تسجيل الدخول")
            return redirect('home')
        else:
            messages.error(request, "معلومات خاطئة")
            return render(request, "loginn.html")
    else:
        return render(request, "loginn.html")
        
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password1")
        password1 = request.POST.get("password2")

        if User.objects.filter(username = username).exists():
            messages.error(request , "إسم المستخدم مستخدم مسبقاً")
            return redirect('signup')
        if password != password1 : 
            messages.error(request, "كلمتا السر غير متطابقتان")
            return redirect('signup')
        user = User.objects.create_user(username = username , 
        password = password)
        login(request , user)
        return redirect("add_address")
    return render(request , "signup.html")


def add_address(request):
    if request.method == "POST":
        phone_no = request.POST.get("phoneno")
        address = request.POST.get("address")
        user = request.user
        save_to_profile = Profile.objects.get(user__id = request.user.id)
        save_to_profile.user = user
        save_to_profile.address = address
        save_to_profile.phone_number = phone_no
        save_to_profile.save()
        return redirect("home")
    return render(request , "add_shipping.html")




def signout(request):
    logout(request)
    return redirect("home")
