from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('main_page/', views.main_page, name='main_page'),
    path('main_page2/', views.main_page2, name='main_page2'),

]

