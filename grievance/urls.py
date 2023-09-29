from django.urls import path
from . import views

urlpatterns = [
    path('submited-grievances/', views.submited_grievances, name="submited-grievances"),
    path('<str:pk>/', views.grievance, name="grievance"),
    path('submit-grievance/', views.submit_grievance, name="submit-grievance"),
]
