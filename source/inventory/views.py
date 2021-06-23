from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib import messages
from .filters import SearchFilter, SearchProduct, SearchSupplier, SearchSold, SearchCustomer
import csv,datetime
from django.http import HttpResponse
from django.db.models import Count
from django.db.models import Sum


# Create your views here.

#@login_required
def home(request):
    title = 'Welcome: This is the Home Page'
    form = 'This is the form variable'
    context = {
        "title": title,
        "test": form
    }
    return render(request, "home.html",context)

@login_required
def receive_products(request):
    title = 'RECEIVE PRODUCTS'
    form = ReceiveProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        #messages.success(request, 'Successfully saved')
        return redirect('/add_rack')
    else:
        form = ReceiveProductForm()
    context = {
        'title': title,
        'form': form
    }
    return render(request, "receive_products.html", context)

@login_required
def list_products(request):
    qset = Product_items_details.objects.all()
    title = 'TOTAL STOCK'
    filt = SearchFilter(request.GET, queryset=qset)
    form = ProductSearchForm(request.GET or None)
    context = {
        'title': title,
        'filter': filt,
        'form': form
    }
    return render(request, "list_products.html", context)





def sell_products(request):
    product_counts = []
    title = 'List of Products'
    products = Products.objects.all()
    filt = SearchProduct(request.GET, queryset=products)
    form = SearchProductsForm(request.GET or None)
    
    for i in range(len(products)):
        product_counts.append((products[i].product_name,Product_items_details.objects.filter(product_item_name=products[i], product_sold=False).count()))
    
    for i in range(len(product_counts)):
        product_details = Products.objects.get(product_name=product_counts[i][0])
        product_details.product_quantity = product_counts[i][1] 
        product_details.save()
    
    context = {
        'title': title,
        'products': products,
        'filter': filt,
        'form': form,
        'product_counts': product_counts,
    }
    return render(request, 'sell_products.html', context)

def sell_qty(request,pk):
    selling_product = Products.objects.get(id=pk)
    all_selling_products = Product_items_details.objects.filter(product_item_name=selling_product, product_sold=False)
    qty = all_selling_products.count()
    context = {
        'title':selling_product.product_name,
        'filter': all_selling_products,
        'quantity': qty
    }
    return render(request, 'sell_qty.html', context)

def issue_product(request,pk):
    product = Product_items_details.objects.get(pk=pk)
    form = UpdateSoldForm(instance=product)
    item_name = product.product_item_name
    category = product.product_item_name.product_category
    supplier = product.purchased_from
    rate = product.selling_price
    warehouse = product.product_in
    if request.method == 'POST':
        form = UpdateSoldForm(request.POST, instance=product)
        product.product_sold = True
        if form.is_valid():
            form.save()
            Product_Rack.objects.get(product=pk).delete()
            messages.success(request, 'Successfully Issued')
            return redirect('/sell_products')
    return render(request, 'issue_product.html', {'title':'ISSUE', 'form':form, 'item_name':item_name, 'category':category, 'supplier': supplier, 'rate':rate, 'warehouse':warehouse})


def add_rack(request):
    form = ReceiveProductForm(request.POST or None)
    product = Product_items_details.objects.last()
    products = Product_Rack.objects.all()
    racks = Rack.objects.filter(warehouse=product.product_in)
    array_racks = []
    for i in range(len(racks)):
        count = 0
        for j in range(len(products)):
            if products[j].rack == racks[i]:
                count = count + 1
        array_racks.append(count)

    arr = []
    for i in range(len(array_racks)):
        if array_racks[i] < racks[i].capacity:
            arr.append(i) 

    if len(arr) > 0:
        rack = racks[arr[0]]
        prod_rack = Product_Rack.objects.create(product=product, rack=rack)
        messages.success(request, 'Successfully Stored in rack: '+rack.name)
        return redirect('receive_products')
    else:
        product = Product_items_details.objects.last().delete()
        messages.warning(request, 'Racks in this warehouse are full, item rejected')
        return redirect('receive_products')
        
    context = {
        'racks': racks,
        'title': 'RECEIVE PRODUCTS',
        'form': form,
    }
    return render(request, 'receive_products.html', context)
    
    
def dashboard(request):
    
    product_details = Product_items_details.objects.all()
    product_count = product_details.count()
    product = Products.objects.all()
    details = product.count()
    supplier = Product_items_details.objects.values('purchased_from').distinct().count()
    sold = Product_items_details.objects.filter(product_sold=True).count()
    available = Product_items_details.objects.filter(product_sold=False).count()
    available1 = Product_items_details.objects.filter(product_sold=False)
    labels = []
    data = []
    labels1 = []
    data1 = []
    label2 = []
    data2 = []

   
    customer = Product_items_details.objects.filter(sold_to__isnull=False)
    customers = customer.values('sold_to').distinct().count()
    queryset =customer.values('sold_to').annotate(Customer=Count('product_item_name_id')).order_by('-Customer')
    for entry in queryset:
        labels.append(entry['sold_to'])
        data.append(entry['Customer'])
    category = Category.objects.all()

    queryset1 = available1.values('product_item_name__product_name').annotate(product=Count('product_item_name_id'))
    for entry in queryset1:
        labels1.append(entry['product_item_name__product_name'])
        data1.append(entry['product'])

    queryset2 = available1.values('product_item_name__product_category__name').annotate(product=Count('product_item_name_id'))
    for entry in queryset2:
        label2.append(entry['product_item_name__product_category__name'])
        data2.append(entry['product'])
       
    total = 0
    for i in product_details:
        total += i.selling_price - i.purchased_price 
    context = {
        'total': total,
        'product_count': product_count,
        'supplier': supplier,
        'sold' : sold,
        'available' :available,
        'product' : product,
        'customers': customers,
        'category' : category,
        'product_details':product_details,
        'labels':labels,
        'data':data,
        'labels1':labels1,
        'data1':data1,
        'label2':label2,
        'data2':data2,


        
    }
    return render(request, 'dashboard.html', context)
    
    

def suppliers(request):
    suppliers = Suppliers.objects.all()
    filt = SearchSupplier(request.GET, queryset=suppliers)
    form = SearchSupplierForm(request.GET or None)
    context = {
        'supplier':suppliers,
        'title': 'SUPPLIERS',
        'filter': filt,
        'form': form,
    }

    return render(request, 'suppliers.html', context)

def sold(request):
    products= Product_items_details.objects.filter(product_sold=True)
    filt= SearchSold(request.GET, queryset=products)
    form = SearchSoldForm(request.GET or None)
   
    context = {
       'products': products,
       'title': 'PRODUCTS SOLD',
       'filter': filt,
       'form': form,
    }
    return render(request, 'sold.html', context)


def customers(request):
    customers = Customers.objects.all()
    fil = SearchCustomer(request.GET, queryset=customers)
    form = SearchCustomerForm(request.GET or None)
    context = {
        'title':'CUSTOMERS',
        'customers':customers,
        'filter': fil,
        'form': form,
    }
    return render(request, 'customers.html', context)


def product_details(request,pk):
    product = Product_items_details.objects.get(id=pk)
    if product.product_sold:
        context = {
            'title': 'PRODUCT DETAILS',
            'product': product,
        }
        return render(request, 'product_details.html', context)
    else:
        rack = Product_Rack.objects.get(product=pk)
        context = {
            'title': 'PRODUCT DETAILS',
            'product': product,
            'rack': rack,
        }
        return render(request, 'product_details.html', context)


def transfer(request,pk):

    product = Product_items_details.objects.get(id=pk)
    form = UpdateWarehouseForm(instance=product)
    products = Product_Rack.objects.all()
    if request.method == 'POST':
        form = UpdateWarehouseForm(request.POST)
        racks = Rack.objects.filter(warehouse=form.data['product_in'])
        array_racks = []
        for i in range(len(racks)):
            count = 0
            for j in range(len(products)):
                if products[j].rack == racks[i]:
                    count = count + 1
            array_racks.append(count)

        arr = []
        for i in range(len(array_racks)):
            if array_racks[i] < racks[i].capacity:
                arr.append(i) 

        if len(arr) > 0:
            if form.is_valid():
                warehouse = Warehouse.objects.get(id=form.data['product_in'])
                form = UpdateWarehouseForm(request.POST, instance=product)
                product.product_in = warehouse
                product.save()
                rack = racks[arr[0]]
                Product_Rack.objects.get(product=pk).delete()
                prod_rack = Product_Rack.objects.create(product=product, rack=rack)
                messages.success(request, 'Successfully transfered to '+warehouse.warehouse_name+', Stored in rack: '+rack.name)
                return redirect('list_products')
        else:
            warehouse = Warehouse.objects.get(id=form.data['product_in'])
            messages.warning(request, warehouse.warehouse_name+' is full')
            return redirect('list_products')
    
    context = {
        'title': 'TRANSFER',
        'pk': pk,
        'product': product,
        'form': form,
    }
    return render(request, 'transfer.html', context)


