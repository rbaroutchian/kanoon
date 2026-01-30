from django.urls import path

from . import views


urlpatterns = [
    # path('',views.movielist,name='cinema_page'),
    path('',views.movieListView.as_view(),name='movie_list'),
    path('<int:pk>/reserve/', views.MovieReserveView.as_view(), name='movie_reserve'),
    path('reserve/receipt/<str:tracking_code>/',views.ReserveReceiptView.as_view(),name='reserve_receipt'),
    # path('reserve/<int:movie_id>/', views.MovieReserveView2.as_view(), name='movie_reserve'),
]