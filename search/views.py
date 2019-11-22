from django.shortcuts import render
from .models import *
import simplejson as json
from django.http import HttpResponse

def search(request):
    item = Items.objects.all()
    brand_list = Items.objects.all().values_list('brand', flat = True).distinct()
    return render(request, 'search.html',{'item' : item,'brand_list':brand_list})

def ajax(request):
    brandName = request.GET['brand']
    categoriesName = request.GET['categories']
    print(brandName)
    output = Items.objects.filter(brand = brandName, categories = categoriesName)
    result = {}
    for itemResult in output:
        result[itemResult.name] = itemResult.name
        print(itemResult.name)
    
    return HttpResponse(json.dumps(result),content_type="application/json")