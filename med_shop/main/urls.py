from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('', views.index, name='home'),
    path('<int:category_id>/', views.index, name='category'),
    path('search/', Search.as_view(), name='search'),
    path('about', views.about, name='about'),
    path('cart', views.show_cart, name='cart'),
    path('cart-add/<int:drug_id>/', cart_add, name='cart-add'),
    path('cart-delete/<int:drug_id>/', cart_delete, name='cart-delete'),
    path('accounts/login/', LoginView.as_view(), name="login"),
    path('accounts/logout/', logout_user, name="logout"),
    path('accounts/profile/', ProfilePage.as_view(), name="profile"),
    path('accounts/register/', RegisterView.as_view(), name="register"),
    path('drug-id=<int:pk>/', views.DrugDetailView.as_view(), name="drug-detail"),
    path('brown/', views.brown, name="brown")
]

