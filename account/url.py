from django.urls import path

from . import views

urlpatterns = [
    path('register',views.RegisterAccount.as_view(),name='register_page'),
    path('login',views.LoginView.as_view(),name='login_page'),
    path('profile',views.EditUserProfilePage.as_view(),name='profile_page'),
    path('logout',views.LogoutView.as_view(),name='logout_page')
]