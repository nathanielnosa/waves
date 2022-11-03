from django.urls import path

from . import views

urlpatterns =[
    path('',views.index,name='index'),
    path('home',views.home,name='home'),
    path('singleCar/<str:id>/',views.singleCar,name='singleCar'),
    path('addCart/<str:id>/',views.addCart,name='addCart'),
    path('myCart/',views.myCart,name='myCart'),
    path('manageCart/<str:id>/',views.manageCart,name='manageCart'),
    path('checkout/',views.checkout,name='checkout'),
    path('payments/<str:id>/',views.payments,name='payments'),
    path('<str:ref>/',views.verify_payment,name='verify-payment'),
    path('search',views.search,name='search'),
    path('clearCart',views.clearCart,name='clearCart'),
]

