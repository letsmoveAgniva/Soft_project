from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from .forms import ProductForm, OrderForm
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
@login_required
def index(request):
    orders=Order.objects.all()
    products=Product.objects.all()
    workers_count=User.objects.all().count()
    orders_count=Order.objects.count()
    products_count=Product.objects.count()
    if request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.staff=request.user
            product=Product.objects.get(id=form.data['product'])
            #change product quantity
            product.quantity-=int(form.data['order_quantity'])
            product.ordered_quantity+=int(form.data['order_quantity'])
            product.save()
            instance.save()
            return redirect('dashboard-index')
    else:
        form=OrderForm()
    context={
        'orders':orders,
        'form':form,
        'products':products,
        'workers_count':workers_count,
        'orders_count':orders_count,
        'products_count':products_count,
    }
    # print(context)
    return render(request, 'dashboard/index.html',context)
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
def product_update(request, pk):
    item=Product.objects.get(id=pk)
    if request.method=='POST':
        form=ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form=ProductForm(instance=item)
    context={
        'form':form
    }
    return render(request, 'dashboard/product_update.html', context)
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




