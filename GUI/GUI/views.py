from django.http import HttpResponse
from django.shortcuts import render
import joblib 

def home(request):
    return render(request,"ui.html")
    cls=joblib.load('prediction.h5')
    lis=[]
    lis.append(request.GET['s-date'])
    lis.append(request.GET['e-date'])
    print(lis)
