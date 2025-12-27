from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BitUserRegisterModel, CustomerHadCoins, UserBuyingCryptoModel, BlockChainLedger
from agents.models import AgentHadCrypto
from admins.models import cryptcurrencyratemodel

# ---------------------------
# User Home Page
# ---------------------------
def users(request):
    return render(request,'users/users.html',{})
def usersignup(request):
    return render(request,'users/usersignup.html',{})

# ---------------------------
# User Registration
# ---------------------------
def bituserregister(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pswd = request.POST.get('pswd')
        username = request.POST.get('username')
        mobile = request.POST.get('mobile')
        pan = request.POST.get('pan')
        state = request.POST.get('state')
        location = request.POST.get('location')
        print("Valid Form = ", email)
        try:
            rslts = BitUserRegisterModel.objects.create(email=email, pswd=pswd, username=username, mobile=mobile,
                                                        pan=pan, state=state, location=location)
            if rslts is None:
                print("Invalid Data ", rslts)
                messages.success(request, 'Email ID already exist, Registration Failed ')
            else:
                print("Valid Data ", rslts)
                messages.success(request, 'Registration Success')
        except:
            messages.success(request, 'Email ID already exist, Registration Failed ')
            return render(request, 'users/usersignup.html', {})
    else:
        print("Invalid Form Data")
        messages.success(request, 'Email ID already exist, Registration Failed ')
    return render(request, 'users/usersignup.html', {})


# ---------------------------
# User Login
# ---------------------------
def userlogincheck(request):
    if request.method == "POST":
        email = request.POST.get('email')
        pswd = request.POST.get('pswd')
        print("Email = ", email, ' Password = ', pswd)
        try:
            check = BitUserRegisterModel.objects.get(email=email, pswd=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.username
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/userpage.html', {})
            else:
                messages.warning(request, 'Your Account is not activated yet.')
                return render(request, 'users/users.html', {})
        except BitUserRegisterModel.DoesNotExist:
            messages.error(request, 'Invalid Email or Password.')
            return render(request, 'users/users.html', {})
        except Exception as e:
            print('Unexpected error:', e)
            messages.error(request, 'Something went wrong. Try again.')
            return render(request, 'users/users.html', {})

    # Default GET request — just show login page
    return render(request, 'users/usersignup.html', {})




# ---------------------------
# Start Trading - show available agents and cryptos
# ---------------------------
def StartUserTrading(request):
    email = request.session.get('email')
    if not email:
        return redirect('userlogincheck')

    agents_crypto = AgentHadCrypto.objects.all()
    return render(request, 'users/UserTrading.html', {'objects': agents_crypto})


# ---------------------------
# User selects quantity of crypto to buy
# ---------------------------
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from admins.models import cryptcurrencyratemodel

def UserBuyQuantity(request):
    if request.method == "POST":
        quantity = request.POST.get('quantity')
        currencyname = request.POST.get('currencyname')
        agentemail = request.POST.get('agentemail')
        print("Crypto =", currencyname, "Agent Email =", agentemail, "Quantity =", quantity)

        # Validate inputs
        if not all([quantity, currencyname, agentemail]):
            return HttpResponse("Missing required fields", status=400)
        try:
            quantity = float(quantity)  # Ensure quantity is a number
        except ValueError:
            return HttpResponse("Invalid quantity value", status=400)

        # Query the model (case-insensitive)
        try:
            getDollers = cryptcurrencyratemodel.objects.get(currencytype__iexact=currencyname)
            coinPrice = getDollers.doller
            blockchain = 11.5
            bitBlock = (coinPrice * blockchain) / 100
            print("Block Bit Money", bitBlock)
            bitMoney = bitBlock + coinPrice
            print("Paid for 1 Bit", bitMoney)
            pay = quantity * bitMoney
            dict = {
                'quantity': quantity,
                'currencyname': currencyname,
                'agentemail': agentemail,
                'bitBlock': round(bitMoney, 2),
                'payableAmmount': round(pay, 2)
            }
            return render(request, 'users/userbuytranscation.html', dict)
        except cryptcurrencyratemodel.DoesNotExist:
            print(f"Currency '{currencyname}' not found in database")
            return HttpResponse(f"Currency '{currencyname}' not found", status=404)
    return HttpResponse("Invalid request method", status=405)
# ---------------------------
# User completes the purchase
# ---------------------------from django.http import HttpResponse
from django.shortcuts import render, redirect
from admins.models import cryptcurrencyratemodel  # If needed elsewhere
from .models import CustomerHadCoins, UserBuyingCryptoModel, BlockChainLedger  # Adjust imports based on your app

def UserBuyingCoins(request):
    email = request.session.get('email')
    customername = request.session.get('loggeduser')
    if not email:
        return redirect('userlogincheck')

    if request.method == 'POST':
        currencyname = request.POST.get('currencyname')
        quantity = request.POST.get('quantity')
        agentemail = request.POST.get('agentemail')
        singlecoingamount = request.POST.get('singlecoingamount')
        payableammount = request.POST.get('payableammount')
        cardnumber = request.POST.get('cardnumber')
        nameoncard = request.POST.get('nameoncard')
        cardexpiry = request.POST.get('cardexpiry')
        cvv = request.POST.get('cvv')

        # Validate inputs
        if not all([currencyname, quantity, agentemail, singlecoingamount, payableammount, cardnumber, nameoncard, cardexpiry, cvv]):
            return HttpResponse("Missing required fields", status=400)

        try:
            quantity = float(quantity)  # Convert to float first
            if not quantity.is_integer():
                return HttpResponse("Quantity must be a whole number", status=400)
            quantity = int(quantity)  # Convert to int if whole
            singlecoingamount = float(singlecoingamount)
            payableammount = float(payableammount)
            cvv = int(cvv)
        except ValueError:
            return HttpResponse("Invalid numeric value for quantity, singlecoingamount, or cvv", status=400)

        # Ledger calculation
        oneBlock = 11.5
        blockChainAmmount = (payableammount / 100) * oneBlock

        # Update agent crypto quantity
        updateAgentCoins(agentemail, currencyname, quantity)  # Ensure this function exists

        # Update user crypto quantity
        userQuantity = checkusercrypto(email, currencyname)  # Ensure this function exists
        if userQuantity == 0:
            CustomerHadCoins.objects.create(currencyName=currencyname, customeremail=email, quantity=quantity)
        else:
            totalQuantity = userQuantity + quantity
            CustomerHadCoins.objects.filter(currencyName=currencyname, customeremail=email).update(quantity=totalQuantity)

        # Record transactions
        UserBuyingCryptoModel.objects.create(
            customername=customername,
            email=email,
            currencyname=currencyname,
            quantity=quantity,
            agentemail=agentemail,
            singlecoingamount=singlecoingamount,
            payableammount=payableammount,
            cardnumber=cardnumber,
            nameoncard=nameoncard,
            cardexpiry=cardexpiry,
            cvv=cvv
        )

        BlockChainLedger.objects.create(
            customeremail=email,
            agentemail=agentemail,
            currencyname=currencyname,
            quantity=quantity,
            paidammout=payableammount,
            blockchainmoney=blockChainAmmount
        )

        dict1 = CustomerHadCoins.objects.filter(customeremail=email)
        dict2 = UserBuyingCryptoModel.objects.filter(email=email)
        return render(request, 'users/userbuyed.html', {"object1": dict1, 'object2': dict2})
    
    return HttpResponse("Invalid request method", status=405)


# ---------------------------
# Helper functions
# ---------------------------
def checkusercrypto(useremail, currencyname):
    try:
        obj = CustomerHadCoins.objects.get(currencyName=currencyname, customeremail=useremail)
        return obj.quantity
    except CustomerHadCoins.DoesNotExist:
        return 0


def updateAgentCoins(agentemail, currencyname, quantity):
    agent_crypto = AgentHadCrypto.objects.get(currencyName=currencyname, useremail=agentemail)
    remaining_quantity = agent_crypto.quantity - quantity
    AgentHadCrypto.objects.filter(currencyName=currencyname, useremail=agentemail).update(quantity=remaining_quantity)
    return remaining_quantity


# ---------------------------
# User Transaction History
# ---------------------------
def UserTransactionsHistory(request):
    email = request.session.get('email')
    if not email:
        return redirect('userlogincheck')

    dict1 = CustomerHadCoins.objects.filter(customeremail=email)
    dict2 = UserBuyingCryptoModel.objects.filter(email=email)
    return render(request, 'users/userbuyed.html', {"object1": dict1, 'object2': dict2})


# users/views.py

from django.shortcuts import render
from datetime import date, timedelta

from .utils.prediction import predict_crypto, CRYPTO_SYMBOLS


def prediction_view(request):
    result = None
    error = None

    today = date.today()
    default_end = today - timedelta(days=1)
    default_start = default_end - timedelta(days=365 * 2)

    # Defaults (for GET request)
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
        "users/prediction.html",
        {
            "crypto_options": CRYPTO_SYMBOLS.keys(),
            "result": result,
            "error": error,
            "default_start": start_date,
            "default_end": end_date,
            "forecast_days": forecast_days,
            "selected_coin": selected_coin,
            "today": today,
        }
    )




