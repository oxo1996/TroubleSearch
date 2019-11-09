from django.shortcuts import render
from .models import Item
from django.core.paginator import Paginator

def skincare(request):
    items = Item.objects
    item_list = Item.objects.all()
    paginator = Paginator(item_list, 9)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'skin.html',{'items' : items, 'posts' : posts})

def changeItem(request):
    item_name = request.POST['product']
    items = Item.objects.filter(name=item_name)
    item_list = Item.objects.filter(name=item_name)
    paginator = Paginator(item_list, 1)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'skin.html',{'items' : items, 'posts' : posts})
    