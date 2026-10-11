from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomerForm, MoneyForm, TransferForm
from .models import Customer, Transaction

def staff_required(view_func):
    return login_required(user_passes_test(lambda u: u.is_staff)(view_func))

def employee_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("dashboard")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active and user.is_staff:
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "Invalid credentials or employee access is not enabled.")
    return render(request, "bank/login.html")

@login_required
def employee_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return redirect("dashboard")

@staff_required
def dashboard(request):
    context = {
        "total_customers": Customer.objects.count(),
        "total_balance": Customer.objects.aggregate(total=Sum("balance"))["total"] or Decimal("0.00"),
        "total_transactions": Transaction.objects.count(),
        "recent_transactions": Transaction.objects.select_related("from_customer", "to_customer", "created_by")[:8],
    }
    return render(request, "bank/dashboard.html", context)

@staff_required
def customer_list(request):
    q = request.GET.get("q", "").strip()
    customers = Customer.objects.all()
    if q:
        from django.db.models import Q
        customers = customers.filter(Q(cust_name__icontains=q) | Q(account_no__icontains=q) | Q(mob_no__icontains=q))
    return render(request, "bank/customer_list.html", {"customers": customers, "q": q})

@staff_required
def customer_create(request):
    form = CustomerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        customer = form.save()
        messages.success(request, f"Customer created. Account number: {customer.account_no}")
        return redirect("customer_detail", pk=customer.pk)
    return render(request, "bank/customer_form.html", {"form": form})

@staff_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    history = Transaction.objects.filter(
        from_customer=customer
    ) | Transaction.objects.filter(to_customer=customer)
    return render(request, "bank/customer_detail.html", {
        "customer": customer, "history": history.distinct()[:20]
    })

def _get_customer(account_no):
    return Customer.objects.filter(account_no=account_no.strip()).first()

@staff_required
def deposit(request):
    form = MoneyForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        amount = form.cleaned_data["amount"]
        customer = _get_customer(form.cleaned_data["account_no"])
        if customer is None:
            form.add_error("account_no", "Account not found.")
        else:
            with transaction.atomic():
                customer = Customer.objects.select_for_update().get(pk=customer.pk)
                customer.balance += amount
                customer.save(update_fields=["balance"])
                Transaction.objects.create(
                    transaction_type="DEPOSIT", to_customer=customer, amount=amount,
                    note=form.cleaned_data["note"], created_by=request.user
                )
            messages.success(request, f"Deposit of ₹{amount:.2f} recorded.")
            return redirect("customer_detail", pk=customer.pk)
    return render(request, "bank/money_form.html", {"form": form, "heading": "Deposit money", "button": "Record deposit"})

@staff_required
def withdraw(request):
    form = MoneyForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        amount = form.cleaned_data["amount"]
        customer = _get_customer(form.cleaned_data["account_no"])
        if customer is None:
            form.add_error("account_no", "Account not found.")
        else:
            with transaction.atomic():
                customer = Customer.objects.select_for_update().get(pk=customer.pk)
                if customer.balance < amount:
                    form.add_error("amount", "Insufficient balance.")
                else:
                    customer.balance -= amount
                    customer.save(update_fields=["balance"])
                    Transaction.objects.create(
                        transaction_type="WITHDRAW", from_customer=customer, amount=amount,
                        note=form.cleaned_data["note"], created_by=request.user
                    )
                    messages.success(request, f"Withdrawal of ₹{amount:.2f} recorded.")
                    return redirect("customer_detail", pk=customer.pk)
    return render(request, "bank/money_form.html", {"form": form, "heading": "Withdraw money", "button": "Record withdrawal"})

@staff_required
def transfer(request):
    form = TransferForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        source_no = form.cleaned_data["from_account"].strip()
        target_no = form.cleaned_data["to_account"].strip()
        amount = form.cleaned_data["amount"]
        if source_no == target_no:
            form.add_error("to_account", "Choose a different destination account.")
        else:
            with transaction.atomic():
                customers = list(Customer.objects.select_for_update().filter(
                    account_no__in=[source_no, target_no]
                ).order_by("pk"))
                by_no = {c.account_no: c for c in customers}
                source, target = by_no.get(source_no), by_no.get(target_no)
                if source is None:
                    form.add_error("from_account", "Source account not found.")
                if target is None:
                    form.add_error("to_account", "Destination account not found.")
                if source and target and source.balance < amount:
                    form.add_error("amount", "Insufficient balance.")
                if source and target and source.balance >= amount:
                    source.balance -= amount
                    target.balance += amount
                    source.save(update_fields=["balance"])
                    target.save(update_fields=["balance"])
                    Transaction.objects.create(
                        transaction_type="TRANSFER", from_customer=source, to_customer=target,
                        amount=amount, note=form.cleaned_data["note"], created_by=request.user
                    )
                    messages.success(request, f"Transfer of ₹{amount:.2f} completed.")
                    return redirect("transaction_list")
    return render(request, "bank/transfer_form.html", {"form": form})

@staff_required
def transaction_list(request):
    transactions = Transaction.objects.select_related(
        "from_customer", "to_customer", "created_by"
    )
    return render(request, "bank/transaction_list.html", {"transactions": transactions[:100]})
