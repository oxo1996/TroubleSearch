from django.shortcuts import render
from .models import Items
import json
from dlmodel.avgtfw2v import *

def load(self):
    with open("/webcrawler/ingredients_in_items") as data_file:
        item = json.load(data_file)
    return item

def information(request):
    
    gender = request.POST['gender']
    product = request.POST.getlist('product')
    symptom = request.POST['symptom']

    imodel = avgtfw2v("dlmodel/symptom_w2v.json", "dlmodel/avgw2v_model.json")
    result = imodel.getResult(symptom,product)
    number = []

    temp = Items.objects.all()
    item = Items.objects.none()
    for pname in result.keys():
        temp.filter(name = pname).sim |= result[pname]["sim"]
        item |= temp.filter(name = pname)
        
        #sim.append(result[pname]["sim"])



    return render(request, 'information.html', {'item' : item},{'result':result})



def inform(request):

    

    #imodel = avgtfw2v("symptom_w2v.json", "avgw2v_model.json")
    
   # result = {}
    #for name in product:
     #   result[name] = imodel.mostSimilar(symptom, name, 3)



    # print(request.POST['product'])
    return render(request, 'information.html')