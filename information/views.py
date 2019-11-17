from django.shortcuts import render
from .models import *
import json
from dlmodel.avgtfw2v import *
from dlmodel.bert_bm25 import *

def load(self):
    with open("/webcrawler/ingredients_in_items") as data_file:
        item = json.load(data_file)
    return item

def information(request):
    with open("webcrawler/items.json") as data_file:    
        items = json.load(data_file)
    #gender = request.POST['gender']
    product = request.POST.getlist('product')
    symptom = request.POST['symptom']
    productCount = len(product)
    productReviews = []

    imodel = avgtfw2v("dlmodel/symptom_w2v.json", "dlmodel/avgw2v_model.json")
    result = imodel.getResult(symptom,product)

    components = component.objects.all()
    components.delete()


    temp = Items.objects.all()
    item = Items.objects.none()

    for productIdx in range(productCount):
        productReviews.append((_mostReview(symptom,product[productIdx],items)))
    
    

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
    


    return render( request, 'information.html', {'item' : item ,'components1':components1,'components2':components2,'components3':components3,'recommendItems':recommendItems,'productReviews':productReviews})

def _recommendItems(symptoms,imodel:avgtfw2v):
    item = Items.objects.none()
    temp = Items.objects.all()
    recommendList = imodel.recommendProduct(symptoms)
    for elem in recommendList:
        item|= temp.filter(name = elem[0])

    return item

def _mostReview(symptom,product,items):
    

    reviewList = []
    result = []
    bert = bert_bm25()
    reviewdata = items[product]["reviews"]
    for review in reviewdata:
        reviewList.append(review[1])
    
    reviewIdx = bert.mostSimilar(symptom, reviewList, 3)
    for idx in reviewIdx:
        result.append(reviewList[idx[0]])
    return result

    
    
