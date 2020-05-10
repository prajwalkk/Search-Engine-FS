from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('pagerank/', views.PageRankView.as_view(), name='pagerank'),
]
