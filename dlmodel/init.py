#from dlmodel import dlmodel
from imodel import imodel
from avgtfw2v import avgtfw2v

if __name__ == '__main__':
    imodel = avgtfw2v("symptom_w2v.json", "avgw2v_model.json")
    print(imodel.getResult("allergy", "히아루로닉 크림"))
    #print(imodel.mostSimilar("allergy", "히아루로닉 크림", 20, ""))
    