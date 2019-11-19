from django.shortcuts import render
from .models import *

def search(request):
    item = Items.objects.all()
    return render(request, 'search.html',{'item' : item})
