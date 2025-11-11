from django.urls import path
from . import views
from users.views import bituserregister,userlogincheck,StartUserTrading,UserBuyQuantity,UserBuyingCoins,UserTransactionsHistory

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
    path('UserPredictionTest/', views.UserPredictionTest, name='UserPredictionTest'),
    path('select_coin/<int:dataset_id>/', views.select_coin, name='select_coin'),
    path('predict_coin/', views.predict_coin, name='predict_coin'),
]