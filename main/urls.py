

from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('car_list', views.car_list, name='car_list'),
    path('add/', views.add_car, name='add_car'),
    path('sold/', views.sold_cars, name='sold_cars'),
    path('expense/', views.expense, name='expense'),
    path(' partial_profit/<int:car_id>/', views. partial_profit, name=' partial_profit'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sell/<int:car_id>/', views.sell_car, name='sell_car'),
    path('delete/<int:car_id>/', views.delete_car, name='delete_car'),
 
]
