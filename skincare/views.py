from django.shortcuts import render
from .models import Item
from .models import IngredientsInItems
from django.core.paginator import Paginator

def skincare(request):
    items = Item.objects
    brand_list = Item.objects.all().values_list('brand', flat = True).distinct()
    item_list = Item.objects.all()
    paginator = Paginator(item_list, 9)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'skin.html', {'brand_list': brand_list, 'items' : items, 'posts' : posts})

def productSearch(request):
    item_brand = request.POST.get('brand',False)
    item_categories = request.POST.get('categories',False)
    brand_list = Item.objects.all().values_list('brand', flat = True).distinct()
    items = Item.objects

    if(item_brand == "전체" and item_categories == "전체"):
        item_list = Item.objects.all()
    elif(item_brand != "전체" and item_categories == "전체"):
        item_list = Item.objects.filter(brand = item_brand)
    elif(item_brand == "전체" and item_categories != "전체"):
        item_list = Item.objects.filter(categories = item_categories)
    else :
        item_list = Item.objects.filter(brand = item_brand, categories = item_categories)
 
    paginator = Paginator(item_list, 9)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'skin.html',{'brand_list': brand_list, 'items' : item_list, 'posts' : posts})

def detail(request):
    name = request.POST.get('iname', False)
    ingrlist =IngredientsInItems.objects.all().filter(item_name = name)
    
    item_brand = request.POST.get('brand',False)
    item_categories = request.POST.get('categories',False)
    return render(request, 'detail.html', {'ingrlist':ingrlist, 'name': name, 'brand' : item_brand, 'categories' : item_categories})