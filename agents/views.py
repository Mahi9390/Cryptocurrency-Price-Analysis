from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Sum
from django.conf import settings
import os

from .models import BitAgentRegisterModel, AgentHadCrypto, AgentBuyCryptoModel
from admins.models import cryptcurrencyratemodel, CurrencyUpdateModel
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




# users/views.py

# agents/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta

from users.utils.prediction import predict_crypto, CRYPTO_SYMBOLS



def prediction_view(request):
    result = None
    error = None

    # Default dates
    today = date.today()
    default_end = today - timedelta(days=1)
    default_start = default_end - timedelta(days=365 * 2)

    # Defaults for form persistence
    selected_coin = "Bitcoin"
    start_date = default_start
    end_date = default_end
    forecast_days = 7

    if request.method == "POST":
        selected_coin = request.POST.get("coin")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        forecast_days = int(request.POST.get("forecast_days", 7))

        try:
            result = predict_crypto(
                coin_name=selected_coin,
                start_date_str=start_date,
                end_date_str=end_date,
                forecast_days=forecast_days
            )
        except Exception as e:
            error = str(e)

    return render(
        request,
        "agents/prediction.html",
        {
            "crypto_options": CRYPTO_SYMBOLS.keys(),
            "result": result,
            "error": error,
            "selected_coin": selected_coin,
            "default_start": start_date,
            "default_end": end_date,
            "forecast_days": forecast_days,
            "today": today,
        }
    )
