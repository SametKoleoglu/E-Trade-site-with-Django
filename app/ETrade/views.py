from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from . models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


# Auth İşlemleri
def Login(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.check_password(password):
                if user is not None:
                    login(request, user)
                    return redirect('index')
                else:
                    messages.error(request, 'User not found')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'index'))
            else:
                messages.error(request, 'Email or password is incorrect')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'index'))
        else:
            messages.error(request, 'Email or password is incorrect')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'index'))

    return render(request, 'user/login.html')


def Register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'index'))

        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'index'))

        elif not User.objects.filter(email=email).exists():
            user = User.objects.create_user(
                username=email, first_name=first_name, last_name=last_name, email=email, password=password)
            user.save()
            login(request, user)
        
        return redirect('index')

    return render(request, 'user/register.html')


def Logout(request):
    logout(request)
    return redirect('login')
    # Kullanıcı çıkış yaptığında kaldığı sayfadan devam eder ancak bir aksilik olması durumunda index sayfasına yönlendirir
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'index'))


@login_required(login_url='/login/')
def profil(request):
    user = User.objects.get(username = request.user)
    profil = Profil.objects.get(user=request.user)
    adress = Adress.objects.get(user=request.user)
    
    
    if request.method == 'POST':
        if request.POST.get('btnSubmit') == 'btnPassword':
            oldPass = request.POST.get('oldPass')
            newPass = request.POST.get('newPass')
            rNewPass = request.POST.get('rNewPass')

            if newPass == rNewPass:
                if user.check_password(oldPass):
                    user.set_password(newPass)
                    user.save()
                    logout(request)
                    return redirect('login')
                else:
                    messages.error(request, 'Old password is incorrect')
            else:
                messages.error(request, 'Passwords do not match')
                
        
        elif request.POST.get('btnsubmit') == 'btnProfile':
            username = request.POST.get('username')
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            email = request.POST.get('email')
            phone_number = request.POST.get('phoneNumber')
            birth_date = request.POST.get('birthDate')
            
            if user.email != email:    
                if not User.objects.filter(email=email).exists():
                    user.username = username
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    profil.phone_number = phone_number
                    profil.birth_date = birth_date
                    user.save()
                    profil.save()
                    return redirect('profile')
                else:
                    messages.error(request, 'Email already exists')
            else:
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                profil.phone_number = phone_number
                profil.birth_date = birth_date
                user.save()
                profil.save()
                return redirect('profile')
            
        elif request.POST.get('btnsubmit') == 'btnAddress':
            address = request.POST.get('address')
            province = request.POST.get('province')
            district = request.POST.get('district')
            neighborhood = request.POST.get('neighborhood')
            postalCode = request.POST.get('postalCode')
            
            adress.address = address
            adress.province = province
            adress.district = district
            adress.neighborhood = neighborhood
            adress.postal_code = postalCode
            adress.save()
            return redirect('profile')

            
    
    context = {
        'profile': profil,
        'adress': adress,
        'productQuantity':productQuantity(request)
    }    
    return render(request, 'user/profile.html',context)


def productQuantity(request):
    if request.user.is_authenticated:
        return BasketProduct.objects.filter(user=request.user)
    else:
        return None

def index(request):
    laptops = Product.objects.filter(product_type=2)
    desktops = Product.objects.filter(product_type=1)
    products = Product.objects.all()
    
    
    if request.method == 'POST':
        productid = request.POST.get('product_id')
        
        product = Product.objects.get(id=productid)
        
        if request.POST.get('submit') == 'btnBasket':
            
            if BasketProduct.objects.filter(product=product).exists():
                basket_product = BasketProduct.objects.get(product=product)
                basket_product.quantity += 1
                basket_product.save()
                return redirect('index')
            else:
                basket_product = BasketProduct.objects.create(user=request.user, product=product, quantity=1)
                basket_product.save()
                return redirect('index')
    
    context = {
        'laptops': laptops,
        'desktops': desktops,
        'products': products,
        'productQuantity':productQuantity(request)
    }
    return render(request, 'eTrade/index.html', context)


def Products(request):

    products = Product.objects.all()
    brands = Brand.objects.all()
    colors = Color.objects.all()
    useTypes = UseType.objects.all()
    processorModels = ProcessorModel.objects.all()
    ramSizes = RamSize.objects.all()
    diskQuantities = DiskQuantity.objects.all()
    productTypes = ProductType.objects.all()
    favoriteProducts = Favorite.objects.all() 

    filters = Q()

    if 'brand' in request.GET:
        brandS = request.GET.getlist('brand')
        for brand in brandS:
            filters |= Q(brand__brand=brand)
            
    if "product_type" in request.GET:
        filters &= Q(product_type=request.GET.get("product_type"))

    if 'color' in request.GET:
        colorS = request.GET.getlist('color')
        for color in colorS:
            filters |= Q(color__color=color)

    if 'use_type' in request.GET:
        use_types = request.GET.getlist('use_type')
        for use_type in use_types:
            filters |= Q(use_type__use_type=use_type)

    if 'processor_model' in request.GET:
        processor_models = request.GET.getlist('processor_model')
        for processor_model in processor_models:
            filters |= Q(processor_model__processor_model=processor_model)

    if 'ram_size' in request.GET:
        ram_sizes = request.GET.getlist('ram_size')
        for ram_size in ram_sizes:
            filters |= Q(ram_size__ram_size=ram_size)

    if 'disk_quantity' in request.GET:
        disk_quantities = request.GET.getlist('disk_quantity')
        for disk_quantity in disk_quantities:
            filters |= Q(disk_quantity__disk_quantity=disk_quantity)
            
    if 'product_type' in request.GET:
        product_types = request.GET.getlist('product_type')
        for product_type in product_types:
            filters |= Q(product_type__product_type=product_type)
            

    if 'price_min' in request.GET and 'price_max' in request.GET  and request.GET.get('price_min') != '':
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')

        if price_min == '':
            price_min = 0
            
        filters &= Q(price__gte=price_min, price__lte=price_max)

    products = Product.objects.filter(filters)
    
    # Add To Basket
    if request.method == 'POST':
        productid = request.POST.get('product_id')
        
        product = Product.objects.get(id=productid)
        
        if request.POST.get('submit') == 'btnBasket':
            
            if BasketProduct.objects.filter(product=product).exists():
                basket_product = BasketProduct.objects.get(product=product)
                basket_product.quantity += 1
                basket_product.save()
                return redirect('products')
            else:
                basket_product = BasketProduct.objects.create(user=request.user, product=product, quantity=1)
                basket_product.save()
                return redirect('products')
            
        elif request.POST.get('submit') == 'btnFavorite':
            if Favorite.objects.filter(product=product).exists():
                favorite = Favorite.objects.get(product=product)
                favorite.delete()
                return redirect('products')
            else:
                favorite = Favorite.objects.create(user=request.user, product=product)
                favorite.save()
                return redirect('products')
            
        
    paginator = Paginator(products, 3)  # Her sayfada 4 ürün olacak!
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)    
      

    context = {
        'products': products,
        'brands': brands,
        'colors': colors,
        'useTypes': useTypes,
        'processorModels': processorModels,
        'ramSizes': ramSizes,
        'diskQuantities': diskQuantities,
        'productTypes': productTypes,
        'favoriteProducts': favoriteProducts,
        'productQuantity':productQuantity(request)
    }

    return render(request, 'eTrade/products.html', context)



def ProductDetail(request, product_id):
    product = Product.objects.get(id=product_id)
    comments = Comment.objects.filter(product=product)
    comment_user = None
    favoriteProducts = Favorite.objects.all()
    
    for comment in comments:
        if comment.user == request.user:
            comment_user = comment.user
            
    
    if request.method == 'POST':
        if request.POST.get('submit') == 'btnBasket':
            productid = request.POST.get('productid')
            quantity = int(request.POST.get('quantity'))
            
            product = Product.objects.get(id=productid)
            
            if BasketProduct.objects.filter(product=product).exists():
                basket_product = BasketProduct.objects.get(product=product)
                basket_product.quantity += quantity
                basket_product.save()
                return redirect(f'/product_detail/{product_id}')
            else:
                basket_product = BasketProduct.objects.create(user=request.user, product=product, quantity=1)
                basket_product.save()
                return redirect(f'/product_detail/{product_id}')
            
        
        elif request.POST.get('submit') == 'btnComment':
            comment = request.POST.get('comment')
            
            new_comment = Comment.objects.create(user=request.user,first_name=request.user.first_name,last_name=request.user.last_name, product=product, comment=comment)
            new_comment.save()
            return redirect(f'/product_detail/{product_id}')
        
        elif request.POST.get('submit') == 'btnFavorite':
            if Favorite.objects.filter(product=product).exists():
                favorite = Favorite.objects.get(product=product)
                favorite.delete()
                return redirect('product_detail', product_id)
            else:
                favorite = Favorite.objects.create(user=request.user, product=product)
                favorite.save()
                return redirect('product_detail', product_id)
            
        elif request.POST.get('submit') == 'commentUpdate':
            comment_id = request.POST.get('comment_id')
            comment = request.POST.get('comment')
            
            update_comment = Comment.objects.get(id=comment_id)
            update_comment.comment = comment
            update_comment.save()
            return redirect(f'/product_detail/{product_id}')

    context = {
        'product': product,
        'comments': comments,
        'comment_user': comment_user,
        'favoriteProducts': favoriteProducts,
        'productQuantity':productQuantity(request)
    }
    return render(request, 'eTrade/product_detail.html', context)



def favorite(request):
    favorites = Favorite.objects.filter(user=request.user)

    context={
        "favorites":favorites
    }

    return render(request, "eTrade/favorite.html",context)

@login_required(login_url='/login/')
def Basket(request):
    basket_products = BasketProduct.objects.filter(user=request.user)
    
    cargo = 30
    product_total_price = 0
    total_price = 0
    for product in basket_products:
        product_total_price += product.quantity * product.product.price
    total_price += cargo + product_total_price        
 
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        
        if request.POST.get('submit') == 'btnDelete':
            basket_product = BasketProduct.objects.get(id=product_id)
            basket_product.delete()
            return redirect('basket')
        
        elif request.POST.get('submit') == 'minus':
            product = BasketProduct.objects.get(id=product_id)
            product.quantity -= 1
            product.save()
            
            return redirect('basket')

        elif request.POST.get('submit') == 'plus':
            product = BasketProduct.objects.get(id=product_id)
            product.quantity += 1
            product.save()
            
            return redirect('basket')
    
    context = {
        'basket_products': basket_products,
        "product_total_price": product_total_price,
        "total_price": total_price,
        "cargo": cargo,
        'productQuantity':productQuantity(request)
    }
    return render(request, 'eTrade/basket.html',context)
