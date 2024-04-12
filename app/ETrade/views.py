from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from . models import *
from django.db.models import Q


def index(request):
    laptops = Product.objects.filter(product_type=2)
    desktops = Product.objects.filter(product_type=1)
    return render(request, 'index.html', {'laptops': laptops,'desktops':desktops})


def Category(request):

    products = Product.objects.all()
    brands = Brand.objects.all()
    colors = Color.objects.all()
    useTypes = UseType.objects.all()
    processorModels = ProcessorModel.objects.all()
    ramSizes = RamSize.objects.all()
    diskQuantities = DiskQuantity.objects.all()

    filters = Q()

    if 'brand' in request.GET:
        brandS = request.GET.getlist('brand')
        for brand in brandS:
            filters |= Q(brand=brand)

    if 'color' in request.GET:
        colorS = request.GET.getlist('color')
        for color in colorS:
            filters |= Q(color=color)

    if 'use_type' in request.GET:
        use_types = request.GET.getlist('use_type')
        for use_type in use_types:
            filters |= Q(use_type=use_type)

    if 'processor_model' in request.GET:
        processor_models = request.GET.getlist('processor_model')
        for processor_model in processor_models:
            filters |= Q(processor_model=processor_model)

    if 'ram_size' in request.GET:
        ram_sizes = request.GET.getlist('ram_size')
        for ram_size in ram_sizes:
            filters |= Q(ram_size=ram_size)

    if 'disk_quantity' in request.GET:
        disk_quantities = request.GET.getlist('disk_quantity')
        for disk_quantity in disk_quantities:
            filters |= Q(disk_quantity=disk_quantity)

    if 'price_min' in request.GET and 'price_max' in request.GET  and request.GET.get('price_min') != '':
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')

        if price_min == '':
            price_min = 0
            
            

        filters &= Q(price__gte=price_min, price__lte=price_max)

    products = Product.objects.filter(filters)  

    context = {
        'products': products,
        'brands': brands,
        'colors': colors,
        'useTypes': useTypes,
        'processorModels': processorModels,
        'ramSizes': ramSizes,
        'diskQuantities': diskQuantities
    }

    return render(request, 'category.html', context)


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


def Profile(request):
    return render(request, 'user/profile.html')


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

        else:
            user = User.objects.create(
                username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.save()
            login(request, user)
            redirect('index')

    return render(request, 'user/register.html')


def Logout(request):
    logout(request)
    # Kullanıcı çıkış yaptığında kaldığı sayfadan devam eder ancak bir aksilik olması durumunda index sayfasına yönlendirir
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'index'))
