from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html',{})
def users(request):
    return render(request,'users.html',{})
def agents(request):
    return render(request,'agents.html',{})
def admins(request):
    return render(request,'admins.html',{})

def usersignup(request):
    return render(request,'users/usersignup.html',{})

def agentsignup(request):
    return render(request,'agents/agentsignup.html',{})

def logout(request):
    return render(request,'index.html',{})

from django.shortcuts import render, get_object_or_404
from admins.models import DatasetUpload


from .ml_model.model_logic import predict_future_prices
import pandas as pd

def list_datasets(request):
    datasets = UploadedDataset.objects.all()
    return render(request, 'cryptobitcoin/datasets.html', {'datasets': datasets})

def select_coin(request, dataset_id):
    dataset = get_object_or_404(UploadedDataset, id=dataset_id)
    df = pd.read_csv(dataset.file.path)
    coin_names = df['crypto_name'].unique()
    return render(request, 'cryptobitcoin/select_coin.html', {'dataset': dataset, 'coins': coin_names})

def predict_prices(request, dataset_id, coin_name):
    dataset = get_object_or_404(UploadedDataset, id=dataset_id)
    predictions = predict_future_prices(dataset.file.path, coin_name)
    return render(request, 'cryptobitcoin/show_predictions.html', {
        'coin_name': coin_name,
        'predictions': predictions
    })
