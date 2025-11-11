from django.urls import path
from . import views
from .views import  select_coin, predict_coin

app_name = 'agents'
urlpatterns = [
    path('agents/', views.agents, name='agents'),
    path('bitagentregister/', views.bitagentregister, name='bitagentregister'),
    path('agentlogincheck/', views.agentlogincheck, name='agentlogincheck'),
    path('AgentBuyCrypto/', views.AgentBuyCrypto, name='AgentBuyCrypto'),
    path('agentbuycurrency/<currencyname>/', views.agentbuycurrency, name='agentbuycurrency'),
    path('AgentTransactions/', views.AgentTransactions, name='AgentTransactions'),
    path('AgentHadCoins/', views.AgentHadCoins, name='AgentHadCoins'),
    path('AgentPredectionTest/',views.AgentPredictionTest,name='AgentPredectionTest'),
    # urls.py
    path('select_coin/<int:dataset_id>/', views.select_coin, name='select_coin'),  
    path('predict_coin/', views.predict_coin, name='predict_coin'),

    # Add show_predictions later
    
    
]
