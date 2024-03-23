from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Order, Information
from .forms import ProductForm, OrderForm, InformationForm, ProductEditForm, OrderUpdateForm
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from random import randint

# Create your views here.
@login_required
def index(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    workers_count = User.objects.all().count()
    orders_count = Order.objects.count()
    products_count = Product.objects.count()
    information = Information.objects.first()  # Assuming there's only one instance
    information_content = information.content if information else ""  # Retrieve th
    # Filter out orders with order_quantity not equal to zero
    cur_orders = []
    cur_products = set()  # Track unique products
    for order in orders:
        if order.product not in cur_products:
            cur_orders.append(order)
            cur_products.add(order.product)

    # Calculate daily selling prices
    cur_daily_selling_prices = []
    for order in cur_orders:
        daily_selling_price = order.product.selling_price * order.product.ordered_quantity
        if daily_selling_price != 0:  # Exclude zero selling prices
            cur_daily_selling_prices.append(daily_selling_price)

    # Calculate profit
    profits = [(order.product.selling_price - order.product.buying_price) * order.order_quantity for order in orders]

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            product = Product.objects.get(id=form.data['product'])
            if int(form.data['order_quantity']) > product.quantity:
                messages.error(request, 'Order quantity exceeds available stock')
            else:
                # Change product quantity
                product.quantity -= int(form.data['order_quantity'])
                product.ordered_quantity += int(form.data['order_quantity'])
                product.save()
                instance.save()
                messages.success(request, 'Order has been placed successfully')
        else:
            form = OrderForm()
    else:
        form = OrderForm()

    context = {
        'orders': orders,
        'cur_orders': cur_orders,
        'form': form,
        'products': products,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
       # 'daily_selling_prices': daily_selling_prices,
        'cur_daily_selling_prices': cur_daily_selling_prices,
        'profits': profits,
        'information_content': information_content,
    }

    return render(request, 'dashboard/index.html', context)

def cart(request):
    cart_orders = Order.objects.filter(status='IN_PROGRESS', staff=request.user) 
    context = {
        'cart_orders': cart_orders,
    }
    return render(request, 'dashboard/cart.html', context)

def checkout(request):
    cart_orders = Order.objects.filter(status='IN_PROGRESS', staff=request.user)
    total_price = sum([order.product.selling_price * order.order_quantity for order in cart_orders])
    context = {
        'total_price': total_price,
    }
    return render(request, 'dashboard/checkout.html', context)

def billing(request):
    cart_orders = Order.objects.filter(status='IN_PROGRESS', staff=request.user)
    total_price = sum([order.product.selling_price * order.order_quantity for order in cart_orders])
    for order in cart_orders:
        order.status = 'COMPLETED'
        order.save()
    
    # use system date and a random number as bill number
    bill_number = f'{datetime.now().strftime("%Y%m%d%H%M%S")}{randint(1000, 9999)}'
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    context = {
        'cart_orders': cart_orders,
        'total_price': total_price,
        'date': date,
        'bill_number': bill_number,
    }
    return render(request, 'dashboard/billing.html', context)

@login_required
def staff(request):
    workers=User.objects.all()
    workers_count=workers.count()
    orders_count=Order.objects.count()
    products_count=Product.objects.count()
    context={
        'workers':workers,
        'workers_count':workers_count,
        'orders_count':orders_count,
        'products_count':products_count,
    }
    return render(request, 'dashboard/staff.html',context)

@login_required
def staff_detail(request, pk):
    workers=User.objects.get(id=pk)
    context={
        'workers':workers
    }
    return render(request, 'dashboard/staff_detail.html',context)

@login_required
def product(request):
    #items=Product.objects.all()
    items=Product.objects.raw('SELECT * FROM dashboard_product')
    workers_count=User.objects.all().count()
    orders_count=Order.objects.count()
    products_count=Product.objects.count()
    if request.method=='POST':
        form=ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name=form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added successfully')
            return redirect('dashboard-product')
    else:
        form=ProductForm()    
    context={
        'items':items,
        'form':form,
        'workers_count':workers_count,
        'orders_count':orders_count,
        'products_count':products_count,
    }
    return render(request, 'dashboard/product.html', context)

@login_required
def product_delete(request, pk):
    item=Product.objects.get(id=pk)
    if request.method=='POST':
        item.delete()
        return redirect('dashboard-product')
    context={
        'item':item
    }
    return render(request, 'dashboard/product_delete.html', context)

@login_required
def order(request):
    orders=Order.objects.all()
    workers_count=User.objects.all().count()
    orders_count=orders.count()
    products_count=Product.objects.count()
    context={
        'orders':orders,
        'workers_count':workers_count,
        'orders_count':orders_count,
        'products_count':products_count,
    }
    return render(request, 'dashboard/order.html',context)




@login_required
def sales_statistics(request):
    orders = Order.objects.all()
    cur_orders = []
    cur_products = set()  # Track unique products
    for order in orders:
        if order.product not in cur_products:
            cur_orders.append(order)
            cur_products.add(order.product)
    statistics = []
    for order in cur_orders:
        profit = order.calculate_profit()
        statistics.append({
            'product': order.product.name,
            'quantity_sold': order.product.ordered_quantity,
            'price_realized': order.product.selling_price,
            'profit': profit,
            'total_selling_price': order.product.ordered_quantity * order.product.selling_price,
        })
    return render(request, 'dashboard/sales_statistics.html', {'statistics': statistics})



def edit_information(request):
    information = Information.objects.first()  # Assuming there's only one instance
    form = InformationForm(request.POST or None, instance=information)
    if form.is_valid():
        form.save()
        return redirect('dashboard-index')  # Redirect to the dashboard or any other page
    return render(request, 'dashboard/edit_information.html', {'form': form})

@login_required
def product_update(request, pk):
    item=Product.objects.get(id=pk)
    if request.method=='POST':
        form=ProductEditForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form=ProductEditForm(instance=item)
    context={
        'form':form
    }
    return render(request, 'dashboard/product_update.html', context)

@login_required
def order_update(request, pk):
    item=Order.objects.get(id=pk)
    if request.method=='POST':
        form=OrderUpdateForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-order')
    else:
        form=OrderUpdateForm(instance=item)
    context={
        'form':form
    }
    return render(request, 'dashboard/order_update.html', context)