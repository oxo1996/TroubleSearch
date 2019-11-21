from django.shortcuts import render
from .models import *
import json
from dlmodel.embedding.w2v_tfidf import W2vTfidf

def load(self):
    with open("/webcrawler/ingredients_in_items") as data_file:
        item = json.load(data_file)
    return item

def information(request):
    
    #gender = request.POST['gender']
    product = request.POST.getlist('product')
    symptom = request.POST['symptom']

    imodel = W2vTfidf("dlmodel/embedding/symptom_w2v.json", "dlmodel/embedding/avgw2v_model.json")
    result = imodel.get_result(symptom,product)

    components = component.objects.all()
    components.delete()


    temp = Items.objects.all()
    item = Items.objects.none()

    recommendItems = _recommendItems(symptom,imodel)
    for elem in result:
        
        #temp.filter(name = elem[0]).sim = result[pname]["sim"]
        item |= temp.filter(name = elem[0])
        for ing in elem[1]["ingr"]:
            component.objects.create(component_name=ing[0],component_sim=str(round(ing[1],3)))
            
        

    components = component.objects.all()
    components1 = components[:3]
    components2 = components[3:6]
    components3 = components[6:9]
    



    return render(request, 'information.html', {'item' : item ,'components1':components1,'components2':components2,'components3':components3,'recommendItems':recommendItems})

def _recommendItems(symptoms, imodel:W2vTfidf):
    item = Items.objects.none()
    temp = Items.objects.all()
    recommendList = imodel.recommend_product(symptoms)
    for elem in recommendList:
        item|= temp.filter(name = elem[0])

    return item

