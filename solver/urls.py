from django.urls import path

from solver import views

urlpatterns = [
    path('', views.index, name='index'),
    path('solver/' , views.solver , name = 'solver') ,  
    path('solving/' , views.solver_init , name = 'solver_init')

]