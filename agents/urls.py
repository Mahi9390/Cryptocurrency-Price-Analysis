from django.urls import path
from . import views

app_name = 'agents'
urlpatterns = [
    path('agents/', views.agents, name='agents'),
    path('bitagentregister/', views.bitagentregister, name='bitagentregister'),
    path('agentlogincheck/', views.agentlogincheck, name='agentlogincheck'),
    path('AgentBuyCrypto/', views.AgentBuyCrypto, name='AgentBuyCrypto'),
    path('agentbuycurrency/<currencyname>/', views.agentbuycurrency, name='agentbuycurrency'),
    path('AgentTransactions/', views.AgentTransactions, name='AgentTransactions'),
    path('AgentHadCoins/', views.AgentHadCoins, name='AgentHadCoins'),
    path('prediction/', views.prediction_view, name='AgentPrediction')
]
