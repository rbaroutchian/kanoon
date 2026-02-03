from django.urls import path

from . import views

urlpatterns = [
    path('register',views.RegisterAccount.as_view(),name='register_page'),
    path('login',views.LoginView.as_view(),name='login_page'),
    path('profile',views.EditUserProfilePage.as_view(),name='profile_page'),
    path('reserv',views.MyReservationsView.as_view(),name='reserv'),
    path('sabtenam',views.ClassPishView.as_view(),name='pish_sabtenam'),
    path('logout',views.LogoutView.as_view(),name='logout_page')
]