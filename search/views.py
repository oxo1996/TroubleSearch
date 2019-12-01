from django.shortcuts import render
from .models import *
import simplejson as json
from django.http import HttpResponse

def search(request):
    item = ItemInfo.objects.all()
    brand_list = Brand.objects.all()
    return render(request, 'search.html',{'item' : item,'brand_list':brand_list})

def ajax(request):
    brandid = request.GET['brand']
    categoryid = request.GET['categories']
    output = ItemInfo.objects.filter(brand_id = brandid, category_id = categoryid)
    result = {}
    for itemResult in output:
        result[itemResult.item_name] = itemResult.item_name
    
    return HttpResponse(json.dumps(result),content_type="application/json")