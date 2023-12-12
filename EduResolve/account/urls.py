from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_account, name="login"),
    path('logout/', views.logout_account, name="logout"),
    path('register/', views.register_student_account, name="register"),
    path('dashboard/', views.account_dashboard, name="dashboard"),

    # Account Verfication & Activation
    path('verify-account/<uidb64>/', views.verify_account, name="verify-account"),
    path('activate-account/<uidb64>/<token>/', views.activate_account, name="activate-account"),
]