from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/logs/', views.get_logs, name='get_logs'),
    path('api/block/<int:log_id>/', views.block_log, name='block_log'),
    path('attack-endpoint/', views.attack_endpoint, name='attack_endpoint'),
]
