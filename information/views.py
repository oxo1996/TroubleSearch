from django.shortcuts import render
from .models import *
import json
from dlmodel.avgtfw2v import *

def load(self):
    with open("/webcrawler/ingredients_in_items") as data_file:
        item = json.load(data_file)
    return item

def information(request):
    
    #gender = request.POST['gender']
    product = request.POST.getlist('product')
    symptom = request.POST['symptom']

    imodel = avgtfw2v("dlmodel/symptom_w2v.json", "dlmodel/avgw2v_model.json")
    result = imodel.getResult(symptom,product)
    print(type(result))

    components = component.objects.all()
    components.delete()


    temp = Items.objects.all()
    item = Items.objects.none()
    for elem in result:
        
        #temp.filter(name = elem[0]).sim = result[pname]["sim"]
        item |= temp.filter(name = elem[0])
        for ing in elem[1]["ingr"]:
            component.objects.create(component_name=ing[0],component_sim=str(round(ing[1],3)))
            
        

    components = component.objects.all()
    components1 = components[:3]
    components2 = components[3:6]
    components3 = components[6:9]
    



    return render(request, 'information.html', {'item' : item ,'components1':components1,'components2':components2,'components3':components3})



def inform(request):

    

    #imodel = avgtfw2v("symptom_w2v.json", "avgw2v_model.json")
    
   # result = {}
    #for name in product:
     #   result[name] = imodel.mostSimilar(symptom, name, 3)



    # print(request.POST['product'])
    return render(request, 'information.html')