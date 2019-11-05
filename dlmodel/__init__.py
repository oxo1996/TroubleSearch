#from dlmodel import dlmodel
from imodel import imodel
from avgtfw2v import avgtfw2v

if __name__ == '__main__':
    imodel = avgtfw2v("symptom_w2v.json", "avgw2v_model.json")
    #print(imodel.getResult("allergy", ["크림 스킨", "타임프리즈 에센스 ex", "딥 씨 워터폴 앰플"]))
    
    print(imodel.recommendProduct("allergy")[0][0])