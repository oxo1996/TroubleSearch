from detector import detector
from SVM_model import SVM_model

if __name__ == '__main__':
    sm = SVM_model("FakeReviewDetector.pkl")
    test_ex = "this is good item"
    print(sm.predict([(sm.toFeatureVector(3, "N", "skincare", sm.preProcess(test_ex)), 'real')]))