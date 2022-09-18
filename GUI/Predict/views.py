from django.shortcuts import render
from .forms import formsubmit
import requests,pandas as pd,numpy as np,matplotlib.pyplot as plt, sys
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

model=load_model('./savedmodel/prediction.h5')
api_key='3a26916aa35b483d9d4e8abf719b08af'
scaler=MinMaxScaler(feature_range=(0,1))
time_interval_train=24
prediction_interval=12
np.set_printoptions(threshold=sys.maxsize)

def bitcoin_pre(test_start,test_end):
    interval= '5min'
    test_api_url=f"https://api.twelvedata.com/time_series?apikey={api_key}&interval={interval}&symbol=BTC/USD&start_date={test_start}&end_date={test_end}"
    test_data= requests.get(test_api_url).json()
    test_data_final=pd.DataFrame(test_data['values'])
    test_inputs= test_data_final['close'].values
    test_inputs= test_inputs.reshape(-1,1)
    model_inputs= scaler.fit_transform(test_inputs)
    x_test=[]
    for x in range(time_interval_train, len(model_inputs)):
        x_test.append(model_inputs[x - time_interval_train:x,0])
    x_test= np.array(x_test)
    x_test= np.reshape(x_test,(x_test.shape[0],x_test.shape[1]))
    bitcoin_prices=pd.to_numeric(test_data_final['close'], errors ='coerce').values
    prediction_prices=model.predict(x_test)
    prediction_prices = np.reshape(prediction_prices,(prediction_prices.shape[0],1))
    prediction_prices= scaler.inverse_transform(prediction_prices)
    last_data= model_inputs[len(model_inputs)+1 - time_interval_train:len(model_inputs)+1,0]
    last_data= np.array(last_data)
    last_data=np.reshape(last_data,(1,last_data.shape[0], 1))
    x=model.predict(last_data)
    x=scaler.inverse_transform(x)
    prediction_prices = np.reshape(prediction_prices,(prediction_prices.shape[0]))
    return(x[0][0], bitcoin_prices, prediction_prices)

def index(request):
    if request.method=='POST':
        form=formsubmit(request.POST)
        if form.is_valid():
            c=form.cleaned_data['s_date']
            d=form.cleaned_data['e_date']
            f=form.cleaned_data['s_time']
            g=form.cleaned_data['e_time']
            start = str(c)+' '+str(f)
            end = str(d)+' '+str(g)
            result, bitPrice, prePrice  = bitcoin_pre(start,end)
            content = {
                'result' : result,
                'bitPrice' : bitPrice,
                'predPrice' : prePrice
            }
            return render(request,'ans.html', content)
    else:
        content={
            "form": formsubmit()
        }

    return render(request,'ui.html', content)

def second(request):
    return render(request,'ui.html')






