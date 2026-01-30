from tkinter.font import names

from django.urls import path

from . import views

urlpatterns= [
    path('',views.index.as_view(), name='home_page'),
    path('about',views.AboutView.as_view(),name='about_page')
]