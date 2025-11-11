from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Sum
from django.conf import settings
import os

from .models import BitAgentRegisterModel, AgentHadCrypto, AgentBuyCryptoModel, AgentPredictionModel
from admins.models import cryptcurrencyratemodel, CurrencyUpdateModel, DatasetUpload
from users.models import BlockChainLedger
from users.lstmann import predictionstart
from users.algo.generatedata import GetData

# -----------------------------
# AGENT REGISTRATION
# -----------------------------

def agents(request):
    return render(request,'agents/agents.html',{})

def agentsignup(request):
    return render(request,'agents/agentsignup.html',{})

def bitagentregister(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pswd = request.POST.get('pswd')
        username = request.POST.get('username')
        mobile = request.POST.get('mobile')
        pan = request.POST.get('pan')
        state = request.POST.get('state')
        location = request.POST.get('location')
        crypttype = request.POST.get('cryptocurrencies')
        print("Valid Form = ", email)
        try:
            rslts = BitAgentRegisterModel.objects.create(email=email, pswd=pswd, username=username, mobile=mobile,
                                                         pan=pan, state=state, location=location,
                                                         cryptcurrency=crypttype)

            if rslts is None:
                print("Invalid Data ", rslts)
                messages.success(request, 'Email ID already exist, Registration Failed ')
            else:
                print("Valid Data ", rslts)
                messages.success(request, 'Registration Success')
        except:
            messages.success(request, 'Email ID already exist, Registration Failed ')
            return render(request, 'agents/agentsignup.html', {})
    else:
        print("Invalid Form Data")
        messages.success(request, 'Email ID already exist, Registration Failed ')
    return render(request, 'agents/agentsignup.html', {})


from django.shortcuts import render, redirect
from django.contrib import messages

def agentlogincheck(request):
    if request.method == "POST":
        email = (request.POST.get('email') or '').strip()
        pswd = (request.POST.get('pswd') or '').strip()
        print("Login attempt — Email:", repr(email), "Password:", repr(pswd))

        # Try to find a matching agent (case-insensitive email)
        agent = BitAgentRegisterModel.objects.filter(email__iexact=email, pswd=pswd).first()

        if agent:
            status = (agent.status or '').strip().lower()
            print("Found agent id:", agent.id, "status:", repr(agent.status))

            if status == "activated":
                # Set session variables
                request.session['id'] = agent.id
                request.session['loggedagent'] = agent.username
                request.session['email'] = agent.email
                print("Login successful for agent id:", agent.id)

                # Prefer redirect to avoid form resubmission
                return render(request, 'agents/agentpage.html', {})  # if you have a named URL for agent dashboard
                # return render(request, 'agents/agentpage.html', {})  # fallback
            else:
                messages.error(request, 'Your account is not activated.')
                return render(request, 'agents/agents.html', {})
        else:
            same_email = BitAgentRegisterModel.objects.filter(email__iexact=email).first()
            if same_email:
                print("Password mismatch for email:", email)
                messages.error(request, 'Invalid password for this email.')
            else:
                print("No account found with email:", email)
                messages.error(request, 'Invalid email or password.')

            return render(request, 'agents/agents.html', {})  # Return login page again

    # For GET request — just show login page
    return render(request, 'agents/agentsignup.html', {})




# agents/views.py
from django.shortcuts import render
from admins.models import DatasetUpload
import os

def AgentBuyCrypto(request):
    dict = cryptcurrencyratemodel.objects.all()
    dict2 = CurrencyUpdateModel.objects.all()
    return render(request, 'agents/buycurrencybyagent.html', {'objects': dict, 'objects1': dict2})


def agentbuycurrency(request, currencyname):
    quntity = int(request.GET.get('quantity'))
    check = cryptcurrencyratemodel.objects.get(currencytype=currencyname)
    currentPrice = check.doller
    payableAmount = quntity * currentPrice
    print("1 Bitcoint value = ", currentPrice, " Currency is = ", currencyname, " Quanity = ", quntity,
          " Payable Ammount = ", payableAmount)
    dict = {
        "currentPrice": currentPrice,
        "currencyname": currencyname,
        "quntity": quntity,
        "PayableAmmount": payableAmount
    }
    return render(request, 'agents/agentbuycrypto.html', dict)


def AgentTransactions(request):
    if request.method == 'POST':
        currencyname = request.POST.get('currencyname')
        currentprice = float(request.POST.get('currentprice'))
        quantity = int(request.POST.get('quantity'))
        payableammount = float(request.POST.get('payableammount'))
        cardnumber = request.POST.get('cardnumber')
        nameoncard = request.POST.get('nameoncard')
        cardexpiry = request.POST.get('cardexpiry')
        cvv = int(request.POST.get('cvv'))
        agentName = request.session['loggedagent']
        email = request.session['email']

        agentQuantities = checkusercrypto(email, currencyname)
        print("Agents Quantity ", agentQuantities)
        if agentQuantities == 0:
            print("AM in IF block")
            AgentHadCrypto.objects.create(currencyName=currencyname, useremail=email, quantity=quantity)
        else:
            totalQuanty = int(agentQuantities) + quantity
            print("AM in else block ",totalQuanty )
            AgentHadCrypto.objects.filter(currencyName=currencyname, useremail=email).update(quantity=totalQuanty)
    AgentBuyCryptoModel.objects.create(agentName = agentName,agentemail=email,currencyname=currencyname,currentprice=currentprice,quantity = quantity,payableammount = payableammount,cardnumber = cardnumber,nameoncard = nameoncard,cardexpiry = cardexpiry,cvv= cvv)
    dict1 = AgentHadCrypto.objects.filter(useremail=email)
    dict2 = AgentBuyCryptoModel.objects.filter(agentemail=email)
    return render(request, 'agents/agentbuyed.html', {"object1": dict1, 'object2': dict2})


def checkusercrypto(useremail, currencyname):
    qty = 0
    try:
        obj = AgentHadCrypto.objects.get(currencyName=currencyname, useremail=useremail)
        qty = obj.quantity
    except Exception as e:
        qty = 0
        print('Error is ', str(e))
    return qty


def AgentHadCoins(request):
    email = request.session['email']
    dict1 = AgentHadCrypto.objects.filter(useremail=email)
    dict2 = AgentBuyCryptoModel.objects.filter(agentemail=email)

    return render(request,'agents/agentbuyed.html',{"object1":dict1,'object2':dict2})

def AgentPredictionTest(request):
    email = request.session.get('email')
    if not email:
        return redirect('agentlogincheck')

    datasets = DatasetUpload.objects.all().order_by('-uploaded_at')[:5]
    return render(request, 'agents/agentpredictionTest.html', {'datasets': datasets})



from django.shortcuts import render, redirect
import ccxt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta
import json  # For passing chart data to template

# Existing list_datasets view...

# agents/views.py
import json
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error

from .models import DatasetUpload



def select_coin(request, dataset_id):
    dataset = get_object_or_404(DatasetUpload, id=dataset_id)
    coins = ['BTC', 'ETH', 'BNB', 'SOL']  # Add more if needed
    return render(request, 'agents/select_coin.html', {
        'dataset': dataset,
        'coins': coins
    })

from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
import pandas as pd
import json
from sklearn.ensemble import RandomForestRegressor

def predict_coin(request):
    if request.method == 'POST':
        dataset_id = request.POST.get('dataset_id')
        coin = request.POST.get('coin')
        dataset = get_object_or_404(DatasetUpload, id=dataset_id)

        # Read CSV
        df = pd.read_csv(dataset.file.path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')

        # 🩵 FIX: Handle duplicate/same-day timestamps (aggregate to daily close)
        df['date'] = df['timestamp'].dt.date
        df = df.groupby('date', as_index=False).agg({'close': 'last'})  # use 'mean' if you prefer daily average
        df['timestamp'] = pd.to_datetime(df['date'])
        df.drop('date', axis=1, inplace=True)

        # Create lag features (previous 3 closing prices)
        df['close_lag1'] = df['close'].shift(1)
        df['close_lag2'] = df['close'].shift(2)
        df['close_lag3'] = df['close'].shift(3)
        df.dropna(inplace=True)

        # Define features and target
        X = df[['close_lag1', 'close_lag2', 'close_lag3']]
        y = df['close']

        # Train Random Forest model
        model = RandomForestRegressor(n_estimators=5, random_state=42)
        model.fit(X, y)

        # Predict next 7 days
        last_3 = df['close'].tail(3).values.tolist()
        predictions = []
        future_dates = []

        last_date = df['timestamp'].iloc[-1]
        current_lag = last_3.copy()

        for i in range(1, 8):
            pred = model.predict([current_lag])[0]
            predictions.append(pred)
            current_lag = current_lag[1:] + [pred]
            next_date = last_date + timedelta(days=i)
            future_dates.append(next_date.strftime('%Y-%m-%d'))

        # Historical data for chart (last 10 days)
        hist_dates = df['timestamp'].tail(10).dt.strftime('%Y-%m-%d').tolist()
        hist_closes = df['close'].tail(10).tolist()

        # Combine historical + predicted data
        chart_labels = hist_dates + future_dates
        chart_historical = hist_closes + [None] * 7
        chart_predicted = [None] * 10 + predictions

        chart_data = json.dumps({
            'labels': chart_labels,
            'datasets': [
                {
                    'label': 'Historical Close',
                    'data': chart_historical,
                    'borderColor': '#007bff',
                    'fill': False
                },
                {
                    'label': f'{coin} Predicted (Next 7 Days)',
                    'data': chart_predicted,
                    'borderColor': '#ff6b6b',
                    'borderDash': [5, 5],
                    'fill': False
                }
            ]
        })

        return render(request, 'agents/predict_coin.html', {
            'coin': coin,
            'chart_data': chart_data,
            'dataset': dataset
        })

    return redirect('agents:AgentPredectionTest')
