from django.shortcuts import render

def component(request):
    return render(request, 'comp.html')
