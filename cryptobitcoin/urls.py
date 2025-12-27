from django.contrib import admin
from django.urls import path, include
from .views import index, usersignup, agentsignup, logout
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin, no namespace or name
    path('', index, name='index'),    # Homepage at root
    path('index/', index, name='index_alt'),  # Alternative name to avoid conflict
    path('logout/', logout, name='logout'),
    path('users/', include('users.urls', namespace='users')),
    path('agents/', include('agents.urls', namespace='agents')),
    path('admins/', include('admins.urls', namespace='admins')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)