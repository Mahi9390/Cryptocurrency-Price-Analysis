from django.urls import path
from .views import (
    adminlogincheck, viewusers, viewagents, activatewaitedusers, activatewaitedagents,
    currentrate, updatecryptocurrency, AdminGetLedger,
    upload_dataset
)
app_name = 'admins'
urlpatterns = [
   

    path('adminlogincheck/',adminlogincheck, name='adminlogincheck'),
    path('viewusers/', viewusers, name='viewusers'),
    path('viewagents/', viewagents, name='viewagents'),
    path('activatewaitedusers/', activatewaitedusers, name='activatewaitedusers'),
    path('activatewaitedagents/', activatewaitedagents, name='activatewaitedagents'),
    path('currentrate/', currentrate, name='currentrate'),
    path('updatecryptocurrency/<curr>/', updatecryptocurrency, name='updatecryptocurrency'),
    path('AdminGetLedger/', AdminGetLedger, name='AdminGetLedger'),
    

    
    


    # Upload dataset
    path('upload_dataset/', upload_dataset, name='upload_dataset'),

    # Admin home
    path('adminhome/', adminlogincheck, name='admins'),
]
