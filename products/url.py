from django.urls import path

from . import views


urlpatterns = [
    # path('',views.productlist,name='product_page'),
    path('',views.productListView.as_view(),name='product_page'),
    path('pishsabt',views.pish_sabtenam.as_view(),name='pishsabt_page'),
    path('<str:slug>/', views.productDetailView.as_view(), name='detail')
]