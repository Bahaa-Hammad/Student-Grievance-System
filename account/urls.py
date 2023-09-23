from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_account, name="login"),
    path('logout/', views.logout_account, name="logout"),
    path('register/', views.register_student_account, name="register"),
    path('dashboard/', views.account_dashboard, name="dashboard"),

]