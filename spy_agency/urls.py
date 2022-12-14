"""spy_agency URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup/", views.SignupPageView.as_view(), name="signup"),
    url(r'^$', views.home_view, name='home'),
    url(r'^hits/$', views.hits_view, name='hits'),
    path('hits/<int:pk>/', views.HitDetailsView.as_view(), name='hit-detail'),
    url(r'^hits-list/$', views.hits_list, name='hits_list'),
    url(r'^hits/create/$', views.create_hit_view, name='create_hit'),
    url(r'^assignment/create/$', views.create_assignment_view, name='create_assignment'),
    url(r'^hitmen/$', views.hitmen_view, name='hitmen'),
    path('hitmen/<int:pk>/', views.HitmenDetailsView.as_view(), name='hitmen-detail'),
    path('assignment/update/<int:pk>/', views.AssignmentUpdateView.as_view(), name='assignment-update'),
    path('hit/update/<int:pk>/', views.HitUpdateView.as_view(), name='hit-update'),
    path('hitmen/update/<int:pk>/', views.HitmenUpdateView.as_view(), name='hitmen-update'),
]
