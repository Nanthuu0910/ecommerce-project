from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from shopapp.models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import datetime


def home(request):
    product=Product.objects.order_by('?')[:9]
    return render(request,'home.html',{'product':product})

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
        return redirect('products')
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
    paginator=Paginator(product_list,5)
    pageno=request.GET.get('page')
    page_object=paginator.get_page(pageno)
    return render(request,'products.html',{'page_object':page_object})


def update_product(request,id):
    product=Product.objects.get(id=id)
    if request.method=='POST':
        product.name=request.POST['name']
        product.price=request.POST['price']
        # description=request.POST['description']
        # if product.image:
        #     product.image.delete()
        if request.FILES.get('image'):
            product.image=request.FILES['image']
        product.save()
        return redirect('seller_dashboard')
    return render(request,'update_product.html',{'product':product})


def delete_product(request,id):
     product=Product.objects.filter(id=id)
     if request.method=='POST':
         product.delete()
         return redirect('seller_dashboard')
     return render(request,'delete_products.html',{'product':product})


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)

    return render(request, 'product_detail.html', {
        'product': product
    })


# def category(request, category):
#     category_obj = Category.objects.get(name=category)
#     products = Product.objects.filter(category=category_obj)
#     subcategories = Category.objects.filter(parent=category_obj)
#     return render(request, 'category.html', {'category': category_obj,'products': products,'subcategories': subcategories})
    
# def add_product(request):
#     if not request.user.is_authenticated:
#         return redirect('login')
#     if request.user.role != 'seller':
#         return redirect('login')
#     categories = Category.objects.all()
#     if request.method == 'POST':
#         name = request.POST['name']
#         category_id = request.POST['category']
#         description = request.POST['description']
#         price = request.POST['price']
#         image = request.FILES.get('image')
#         category = Category.objects.get(id=category_id)
#         Product.objects.create(seller=request.user,category=category,name=name,description=description, price=price,image=image)
#         return redirect('seller_dashboard')
#     return render(request,'add_product.html',{'categories': categories})






# def add_product(request):
#     categories = Category.objects.filter(parent__isnull=True)
#     subcategories = Category.objects.none()
#     selected_category = ""

#     if request.method == "POST":
#         action = request.POST.get("action")
#         if action == "show_subcategories":
#             selected_category = request.POST.get("main_category", "")

#             if selected_category:
#                 subcategories = Category.objects.filter(parent_id=selected_category)
#         elif action == "add_product":
#             name = request.POST.get("name")
#             subcategory_id = request.POST.get("subcategory")
#             description = request.POST.get("description")
#             price = request.POST.get("price")
#             image = request.FILES.get("image")
#             category_obj = Category.objects.filter(id=subcategory_id,parent__isnull=False)[0]
#             Product.objects.create(seller=request.user,category=category_obj,name=name,description=description, price=price,image=image)
#             return redirect("seller_dashboard")
#     return render(request, "add_product.html", {"categories": categories,"subcategories": subcategories,"selected_category": selected_category})


def add_product(request):
    categories = Category.objects.filter(parent__isnull=True)
    subcategories = Category.objects.none()
    selected_category = ""

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "show_subcategories":
            selected_category = request.POST.get("main_category", "")

            if selected_category:
                subcategories = Category.objects.filter(parent_id=selected_category)

        elif action == "add_product":
            name = request.POST.get("name")
            subcategory_id = request.POST.get("subcategory")
            description = request.POST.get("description")
            price = request.POST.get("price")
            image = request.FILES.get("image")

            category_obj = Category.objects.filter(id=subcategory_id,parent__isnull=False).first()

            if category_obj:
                Product.objects.create(seller=request.user,category=category_obj,name=name,description=description,price=price, image=image)
                return redirect("seller_dashboard")

    return render(request, "add_product.html", {"categories": categories,"subcategories": subcategories, "selected_category": selected_category})


def category(request,category):
    try :
        category_obj = Category.objects.filter(name__iexact=category)[0]
    except :
        # messages.error('No products available')
        return redirect('home')
    
    print(category_obj,category)
    subcategories = Category.objects.filter(parent=category_obj.id)
    # products = Product.objects.filter(category=category_obj)

    # products = Product.objects.filter(category__in=subcategories) | products
    products=Product.objects.filter(
        Q(category=category_obj) | Q(category__in=subcategories)
    ).distinct()
    
    print(category_obj)
    print(products)
    print(subcategories)
   
    return render(request, "category.html", {"category": category_obj,"products": products,"subcategories": subcategories})

def search(request):
    if request.method=='POST':
        search=request.POST.get('search')
        product_list=Product.objects.filter(name__icontains=search)
        paginator=Paginator(product_list,5)
        pageno=request.GET.get('page')
        page_object=paginator.get_page(pageno)
        return render(request,'products.html',{'page_object':page_object})
    return redirect('products')

@login_required
def wishlist(request,id):
    print('llll')
  
    product=Product.objects.filter(id=id)
    print('hhh')
    if not product.exists():
        return redirect('product_detail',product_id=id)

    demo=Wishlist.objects.filter(Q(user=request.user) & Q(product=product[0].id))
    if demo.exists():
        demo.delete()
    else:
        Wishlist.objects.create(user=request.user,product=product[0]).save()
    return redirect('product_detail',product_id=id)

@login_required
def add_to_cart(request,id):
    if request.method=='POST':
        product=Product.objects.get(id=id)
        item=Cart.objects.filter(user=request.user,product=product).exclude(id__in=Order.objects.filter(user=request.user).values_list("cart_id",flat=True)).first()
        print(item)
        if item:
            print('hiii')
            item.quantity+=1
            item.total=item.quantity*item.product.price
            item.save()
        else:
            Cart.objects.create(user=request.user,product=product,quantity=1,total=product.price).save()
    return redirect('cart')

@login_required
def cart(request):
    print(Order.objects.filter(user=request.user).values_list("id"))
    items = Cart.objects.filter(user=request.user).exclude(id__in=Order.objects.filter(user=request.user).values_list("cart_id",flat=True))
    print(items)
    return render(request, 'cart.html', {'items': items})
def remove_cart(request,id):
    if request.method=='POST':
        Cart.objects.get(id=id,user=request.user).delete()
    return redirect('cart')
@login_required
def quantity_change(request,id):
    if request.method=='POST':
        item=Cart.objects.get(user=request.user,id=id)
        option=request.POST.get('option')
        if item:
            if option=='increase':
                item.quantity+=1
            elif option=='decrease':
                if item.quantity-1==0:
                    item.delete()
                    return redirect('cart')
                item.quantity-=1
            item.save()
        return redirect('cart')
@login_required       
def buy(request):
    if request.method=='POST':
        item=Cart.objects.filter(user=request.user)
        for i in item:
            Order.objects.create(user=request.user,cart=i,status='pending',payment='False',time=datetime.datetime.now())
        return redirect('order') 
    order=Order.objects.filter(user=request.user)
    return render(request,'order.html',{'order':order}) 

@login_required 
def orderdetails_seller(request):
    if request.user.role!='seller':
        return redirect('login')
    order=Order.objects.filter(cart__product__seller=request.user)
    return render(request,'order_details.html',{'order':order})
@login_required
def allwishlist(request):
    wishlist=Wishlist.objects.filter(user=request.user)
    return render(request,'wishlist.html',{'wishlist':wishlist})

def user_logout(request):
    print('Welcome')
    logout(request)
    return redirect('login')
