from django.shortcuts import render

def symptom(request):
    return render(request, 'symp.html')
