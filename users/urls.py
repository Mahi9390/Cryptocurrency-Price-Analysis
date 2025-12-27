from django.urls import path
from . import views
from users.views import bituserregister,userlogincheck,StartUserTrading,UserBuyQuantity,UserBuyingCoins,UserTransactionsHistory,prediction_view

app_name = 'users'
urlpatterns = [
    path('', views.users, name='users'),  # <-- This is the default /users/ URL
    path('bituserregister/', bituserregister, name='bituserregister'),
    path('signup/',views.usersignup, name='usersignup'),
    path('userlogincheck/', userlogincheck, name='userlogincheck'),
    path('StartUserTrading/', StartUserTrading, name='StartUserTrading'),
    path('UserBuyQuantity/', UserBuyQuantity, name='UserBuyQuantity'),
    path('UserBuyingCoins/', UserBuyingCoins, name='UserBuyingCoins'),
    path('UserTransactionsHistory/', UserTransactionsHistory, name='UserTransactionsHistory'),
    path('prediction/', prediction_view, name='UserPrediction'),
]