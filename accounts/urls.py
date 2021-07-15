from django.urls import path, include

from . import views

urlpatterns = [
    path('login',views.login,name = 'login'),
    path('signup',views.signup,name = 'signup'),
    path('signup_admin',views.signup_admin,name = 'signup_admin'),
    path('logout',views.logout,name = 'logout'),
]
