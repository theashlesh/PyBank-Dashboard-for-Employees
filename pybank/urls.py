from django.contrib import admin
from django.urls import path, include
from bank import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", views.employee_login, name="login"),
    path("accounts/logout/", views.employee_logout, name="logout"),
    path("", views.dashboard, name="dashboard"),
    path("customers/", views.customer_list, name="customer_list"),
    path("customers/new/", views.customer_create, name="customer_create"),
    path("customers/<int:pk>/", views.customer_detail, name="customer_detail"),
    path("transactions/", views.transaction_list, name="transaction_list"),
    path("transactions/deposit/", views.deposit, name="deposit"),
    path("transactions/withdraw/", views.withdraw, name="withdraw"),
    path("transactions/transfer/", views.transfer, name="transfer"),
]
