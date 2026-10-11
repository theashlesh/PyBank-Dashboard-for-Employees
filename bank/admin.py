from django.contrib import admin
from .models import Customer, Transaction

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("cust_name", "account_no", "mob_no", "balance", "created_at")
    search_fields = ("cust_name", "account_no", "mob_no")
    readonly_fields = ("account_no", "created_at")

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "transaction_type", "from_customer", "to_customer", "amount", "created_at")
    list_filter = ("transaction_type", "created_at")
    readonly_fields = ("transaction_type", "from_customer", "to_customer", "amount", "note", "created_by", "created_at")
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
