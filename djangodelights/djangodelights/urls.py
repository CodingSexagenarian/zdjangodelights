"""djangodelights URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path

from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("logout/", views.log_out, name="logout"),
    path('accounts/login/', auth_views.LoginView.as_view(), name="login"),
    path('', views.HomeView.as_view(), name='home'),
    path('ingredients/', views.IngredientsView.as_view(), name="ingredients"),
    path('ingredients/new', views.NewIngredientView.as_view(), name="add_ingredient"),
    path('ingredients/<slug:pk>/update', views.UpdateIngredientView.as_view(), name="update_ingredient"),
    path('ingredients/<pk>/delete', views.DeleteIngredientView.as_view(),
         name="delete_ingredient"),
    path('menu/', views.MenuView.as_view(), name="menu"),
    path('menu/new', views.NewMenuItemView.as_view(), name="add_menu_item"),
    path('reciperequirement/new', views.NewRecipeRequirementView.as_view(), name="add_recipe_requirement"),
    path('purchases/', views.PurchasesView.as_view(), name="purchases"),
    path('purchases/new', views.NewPurchaseView.as_view(), name="add_purchase"),
    path('reports', views.ReportView.as_view(), name="reports")
]