from django.shortcuts import render
from .models import *
import json
from dlmodel.embedding.w2v_tfidf import W2vTfidf
from dlmodel.embedding.w2v_tfidf import *
from dlmodel.embedding.bert_bm25 import *
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

    imodel = W2vTfidf("dlmodel/embedding/symptom_w2v.json", "dlmodel/embedding/avgw2v_model.json")
    result = imodel.get_result(symptom,product)

    components = component.objects.all()
    components.delete()

    temp = Items.objects.all()
    item = Items.objects.none()

    productCount = len(product)
    productReviews = []

    for productIdx in range(productCount):
        productReviews.append((_mostReview(symptom,product[productIdx],items)))

    recommendItems = _recommendItems(symptom,imodel)
    recommend1 = recommendItems.filter(categories = "toner")[:1]
    recommend2 = recommendItems.filter(categories = "lotion")[:1]
    recommend3 = recommendItems.filter(categories = "cream")[:1]

    for elem in result:
        
        #temp.filter(name = elem[0]).sim = result[pname]["sim"]
        item |= temp.filter(name = elem[0])
        for ing in elem[1]["ingr"]:
            component.objects.create(component_name=ing[0],component_sim=str(round(ing[1],3)))
            
        

    components = component.objects.all()
    components1 = components[:3]
    components2 = components[3:6]
    components3 = components[6:9]

    return render(request, 'information.html', {'item' : item ,'components1':components1,'components2':components2,'components3':components3,'recommend1':recommend1, 'recommend2':recommend2, 'recommend3':recommend3 ,'productReviews':productReviews})

def _recommendItems(symptoms, imodel:W2vTfidf):
    item = Items.objects.none()
    temp = Items.objects.all()
    recommendList = imodel.recommend_product(symptoms)
    for elem in recommendList:
        item|= temp.filter(name = elem[0])

    return item

def _mostReview(symptom,product,items):
    
    reviewList = []
    result = []
    bert = BertBm25()
    reviewdata = items[product]["reviews"]
    for review in reviewdata:
        reviewList.append(review[1])
    
    reviewIdx = bert.most_similar(symptom, reviewList, 3)
    for idx in reviewIdx:
        result.append(reviewList[idx[0]])
    return result

