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