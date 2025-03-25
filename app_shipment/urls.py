from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('track/', views.track, name='track'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('changeStatus/', views.changeStatus, name='changeStatus'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('update-status/<int:shipment_id>/', views.update_status, name='update_status'),
    # path('search/', views.home, name='search_result'),  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
