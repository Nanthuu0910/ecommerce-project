from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from shopapp.models import *

def home(request):
    return render(request,'home.html')

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        # role=request.POST['role']
        print(username,email,password,confirm_password)
        if password != confirm_password:
            messages.error(request,'Password does not match')
            return redirect(register)
        user = CustomUser.objects.create_user(username=username,email=email,password=password,role='user')
        return redirect("login")

    return render(request,"register.html")

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            if user.role=='admin':
                return redirect('admin_dashboard')
            elif user.role=='seller':
                return redirect('seller_dashboard')

            else:
                return redirect('user_dashboard')  
        else:
            messages.error(request, 'Enter valid username or password')
            return redirect('login')
        
    return render(request,'login.html')

def become_seller(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if Seller.objects.filter(user=request.user).exists():
        return redirect('status_info')
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        shop_name = request.POST['shop_name']
        phone = request.POST['phone']
        address =request.POST['address']
        pic=request.FILES['pic']  
        print("user", request.user)
        print("id:", request.user.id)
        print("authenticate:", request.user.is_authenticated)
        Seller.objects.create(user=request.user,name=name,email=email,shop_name=shop_name,phone=phone,address=address,pic=pic,status='pending'
)
        return redirect('status_info')
    return render(request,'become_seller.html')

def status_info(request):
    return render(request,'status_info.html')

def user_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.role != 'user':
        return redirect('login')
    return render(request,'user_dashboard.html')

def seller_dashboard(request):
    if not request.user.is_authenticated:
        return redirect(login)
    if request.user.role !='seller':
        return redirect(products)
    products=Product.objects.filter(seller=request.user)
    return render(request,'seller_dashboard.html',{'products':products})

def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.role != 'admin':
        return redirect('login')
    
    # application = Seller.objects.all()
    # print("SELLER APPLICATIONS:", application)
    # print("COUNT:", application.count())

    application=Seller.objects.filter(status='pending')
    return render(request,'admin_dashboard.html',{'applications':application })
def admin_accept(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.role != 'admin':
        return redirect('login') 
    application=Seller.objects.get(id=id)
    application.status='approved'
    user=CustomUser.objects.get(id=application.user.id)
    user.role='seller'
    user.status='approved'
    user.save()
    application.save()
    return redirect('admin_dashboard')

def products(request):
    product_list=Product.objects.all()
    return render(request,'products.html',{'products':product_list})


def user_logout(request):
    print('Welcome')
    logout(request)

    return redirect('login')