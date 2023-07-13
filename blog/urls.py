from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup , name='signup'),
    path('login', views.login , name='login'),
    path('logout', views.logout , name='logout'),
    path('create', views.create , name='create'),
    path('read/<str:id>', views.read, name='read'),
    path('delete/<str:id>', views.delete, name='delete'),
    path('edit/<str:id>', views.edit, name='edit'),
    path('contact', views.contact.as_view(), name='contact'),
]