from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
import json

def skincare(request):
    brand_list = Brand.objects.all()
    items = ItemInfo.objects.all()
    
    paginator = Paginator(items, 9)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'skin.html', {'brand_list': brand_list, 'items' : items, 'posts' : posts})

def productSearch(request):
    item_brand = request.POST.get('brand')
    item_categories = request.POST.get('categories')
    brand_list = Brand.objects.all()

    if(item_brand == '10' and item_categories == '10'):
        item_list = ItemInfo.objects.all()
    elif(item_brand != '10' and item_categories == '10'):
        item_list = ItemInfo.objects.filter(brand_id = item_brand)
    elif(item_brand == '10' and item_categories != '10'):
        item_list = ItemInfo.objects.filter(category_id = item_categories)
    else :
        item_list = ItemInfo.objects.filter(brand_id = item_brand, category_id = item_categories)
    

    paginator = Paginator(item_list, 9)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'skin.html',{'brand_list': brand_list, 'posts' : posts})

def detail(request):
    itemid = request.POST.get('id', False)
    item = ItemInfo.objects.filter(item_id = itemid)
    ingrlist = IngrInfo.objects.filter(item = itemid)
    '''
    with open("webcrawler/items.json") as data_file:
        items = json.load(data_file)
    temp_reviews = items[itemid]["reviews"]
    raw_reviews = []
    for data in temp_reviews:
        raw_reviews.append(data[1])'''
    raw_reviews = ReviewInfo.objects.filter(item = itemid)

    return render(request, 'detail.html', {'ingrlist':ingrlist, 'reviews':raw_reviews, 'item': item})