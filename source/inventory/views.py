from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib import messages
from .filters import SearchFilter, SearchProduct, SearchSupplier, SearchSold, SearchOrders, SearchCustomers, SearchEmployee
import csv,datetime
from django.http import HttpResponse
from django.db.models import Count
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .decorators import *
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import numpy as np

# Create your views here.

#@login_required
@authenticate_user
def home(request):
    title = 'Welcome: This is the Home Page'
    form = 'This is the form variable'
    context = {
        "title": title,
        "test": form
    }
    return render(request, "home.html",context)
    
@authenticate_superuser
@authenticate_user
def receive_products(request):
    title = 'RECEIVE PRODUCTS'
    form = ReceiveProductForm(request.POST or None)
    items_received = []
    if form.is_valid():
        form.save(commit=False)
        product_item_name = form.cleaned_data.get('product_item_name')
        purchased_from = form.cleaned_data.get('purchased_from')
        purchased_price = form.cleaned_data.get('purchased_price')
        selling_price = form.cleaned_data.get('selling_price')
        product_in = form.cleaned_data.get('product_in')
        quantity = form.cleaned_data['quantity']
        
        current_item = Products.objects.get(id=form.cleaned_data['product_item_name'].id)
        currrent_item_vol = product_volume(current_item)
        total_entry_vol = quantity * currrent_item_vol

        print(total_entry_vol)
        print(total_entry_vol)

        racks = Rack.objects.filter(warehouse=product_in)
        available_rooms = []
        for i in range(len(racks)):
            if racks[i].available_storage_vol > total_entry_vol:
                available_rooms.append(racks[i])
        if len(available_rooms) > 0:
            product = Products.objects.get(id=product_item_name.id)
            for i in range(quantity):
                Product_items_details.objects.create(product_item_name=product_item_name,
                                                    purchased_from=purchased_from,
                                                    purchased_price=purchased_price,
                                                    selling_price=selling_price,
                                                    product_in=product_in,
                                                    room=available_rooms[0])
                product.product_quantity = product.product_quantity + 1
                product.save()
            #print("Quantity ", product.product_name, product.product_quantity)
            room = Rack.objects.get(id=available_rooms[0].id)
            room.available_storage_vol = room.available_storage_vol - total_entry_vol
            room.save()
            redirect('/receive_products')
            messages.success(request, "successfully stored in "+str(product_in)+" "+str(available_rooms[0]))
        else:
            messages.warning(request,"insufficient storage, try reducing quantity")
    else:
        form = ReceiveProductForm()
    context = {
        'title': title,
        'form': form
    }
    return render(request, "receive_products.html", context)

def product_volume(product):
    return product.product_length_cm*product.product_width_cm*product.product_height_cm


@login_required
@authenticate_superuser
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




@login_required
@authenticate_superuser
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

@login_required
@authenticate_superuser
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

@login_required
@authenticate_superuser
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
    
 
@login_required   
@authenticate_superuser 
def dashboard(request):
    product_details = Product_items_details.objects.all()
    product_count = product_details.count()
    employee=Employee.objects.all().count()
    product = Products.objects.all()
    customers  = Customers.objects.all()
    order=ProductOrder.objects.all()
    product_details = Product_items_details.objects.all()
    order1=order.distinct().count()
    c=customers.all().count()
    details = product.count()
    supplier = Product_items_details.objects.values('purchased_from').distinct().count()
    category = Category.objects.all()
    labels1 = []
    data1 = []
    label2 = []
    data2 = []
    

    queryset2 = product_details.values('product_item_name__product_category__name').annotate(product=Count('product_item_name_id'))
    for entry in queryset2:
        label2.append(entry['product_item_name__product_category__name'])
        data2.append(entry['product'])

   
       
    context = {
        'product_count': product_count,
        'supplier': supplier,
        'product' : product,
        'employee': employee,
        'category' : category,
        'order':order,
        'order1':order1,
        'c':c,
        'product_details':product_details,
        'labels1':labels1,
        'data1':data1,
        'label2':label2,
        'data2':data2,
       

        
    }
    return render(request, 'dashboard.html', context)
    
    
@login_required
@authenticate_superuser
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

@login_required
@authenticate_superuser
def product_details(request,pk):
    product = Product_items_details.objects.get(id=pk)
    if product.product_sold:
        context = {
            'title': 'PRODUCT DETAILS',
            'product': product,
        }
        return render(request, 'product_details.html', context)
    else:
        context = {
            'title': 'PRODUCT DETAILS',
            'product': product
        }
        return render(request, 'product_details.html', context)


@login_required
@authenticate_superuser
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

@login_required
def place_orders(request):
    title = "Products"
    products = Products.objects.all()
    context = {
        'title': title,
        'products': products,
    }
    return render(request, "place_orders.html", context)

def customer_login(request):
    title = "Customer Login"
    form = CustomerLoginForm(request.GET or None)
    context = {
        'title':title,
        'form':form,
    }
    return render(request, "customer_login.html", context)

def customer_registration(request):
    title = "Customer Registration"
    form = CustomerRegistrationForm(request.POST or None)
    if form.is_valid():
        form.save(commit=False)
        name = form.cleaned_data.get('name')
        state = form.cleaned_data.get('state') 
        city = form.cleaned_data.get('city') 
        pincode = form.cleaned_data.get('pincode') 
        address = form.cleaned_data.get('address') 
        username = form.cleaned_data.get('username') 
        password = form.cleaned_data.get('password')
        confirm_password = form.cleaned_data.get('confirm_password')
        if password == confirm_password:
            pword = make_password(password)
            User.objects.create(username=username, password=pword)
            user = User.objects.last() 
            Customers.objects.create(user=user, name=name, state=state, 
                                    city=city, pincode=pincode, address=address, username=username, 
                                    password=password)
            messages.success(request,"Registration Successful")
            return redirect('/place_orders')
        else:
            messages.warning(request,"password did not match")
    else:
        print("validation failed")
    context = {
        'title':title,
        'form':form,
    }
    return render(request, "customer_registration.html", context)


def maps(request):
    title = "lets do maps"
    form = GeoForm(request.POST or None)
    geolocator = Nominatim(user_agent='Measurements')

    if form.is_valid():
        instance = form.save(commit=False)
        location = geolocator.geocode(form.cleaned_data.get('location'))
        destination = geolocator.geocode(form.cleaned_data.get('destination'))
        print(location)
        print(location.latitude)
        print(location.longitude)
        print("######################")
        print(destination)
        print(destination.latitude)
        print(destination.longitude)

        l_lat = location.latitude
        l_lon = location.longitude
        d_lat = destination.latitude
        d_lon = destination.longitude

        pointA = (l_lat, l_lon)
        pointB = (d_lat, d_lon)

        distance = round(geodesic(pointA, pointB).km, 2)
        print("************")
        print("distance", distance)

    context = {
        'title': title,
        'form': form,
    }

    return render(request, "maps.html", context)



def order(request,pk):
    title = "Place Order"
    product = Products.objects.get(id=pk)
    products = Product_items_details.objects.filter(product_item_name=product, product_sold=False, reserved=False)
    total_price = 0
    rate = calculate_rate(products)
    form = ProductOrderForm(request.POST or None)
    customer = Customers.objects.filter(user=request.user)
    warehouse = calculate_distance(customer[0].city,customer[0].state)
    if form.is_valid():
        form.save(commit=False)
        quantity = form.cleaned_data.get('quantity')
        if quantity > product.product_quantity:
            messages.warning(request, "only "+str(product.product_quantity)+" "+product.product_name+"'s are available")
        else:
            total_amt = quantity*rate
            
            items = Product_items_details.objects.filter(product_item_name=product, 
                                                        product_sold=False, 
                                                        reserved=False, 
                                                        product_in=warehouse).order_by('id')[:quantity]
            if len(items) < 1:
                items = Product_items_details.objects.filter(product_item_name=product, 
                                                        product_sold=False, 
                                                        reserved=False).order_by('id')[:quantity]
                ProductOrder.objects.create(customer=customer[0], 
                                        warehouse=items[0].product_in, 
                                        product=product, 
                                        quantity=quantity, 
                                        order_total_amt=total_amt)
            else:
                ProductOrder.objects.create(customer=customer[0], 
                                        warehouse=warehouse, 
                                        product=product, 
                                        quantity=quantity, 
                                        order_total_amt=total_amt)
            order = ProductOrder.objects.last()
            for i in range(len(items)):
                #form2 = UpdateSoldForm(request.POST, instance=items[i])
                items[i].reserved = True
                items[i].order_id = order
                items[i].save()
            product.product_quantity = product.product_quantity - quantity
            product.save()
            messages.success(request,"Order Placed Successfully")
    context = {
        'title': title,
        'product':product,
        'rate':rate,
        'form':form,
    }
    return render(request, "order.html", context)


def calculate_rate(list_):
    total_price = 0
    for i in range(len(list_)):
        total_price = total_price + list_[i].selling_price
    rate = total_price/len(list_)
    return rate

def calculate_distance(customer_city, customer_state):  
    geolocator = Nominatim(user_agent='Inventory')
    distance = []
    warehouse = Warehouse.objects.all()
    for i in range(len(warehouse)):
        location = geolocator.geocode(customer_city+" "+customer_state)
        destination = geolocator.geocode(warehouse[i].warehouse_address)
        l_lat = location.latitude
        l_lon = location.longitude
        d_lat = destination.latitude
        d_lon = destination.longitude
        pointA = (l_lat, l_lon)
        pointB = (d_lat, d_lon)
        distance.append(round(geodesic(pointA, pointB).km, 2)) 
    print(distance)
    return warehouse[int(np.argmin(distance))]
    #location = geolocator.geocode(form.cleaned_data.get('location'))
    #destination = geolocator.geocode(form.cleaned_data.get('destination'))


def view_orders(request):
    title = "Your Orders"
    customer = Customers.objects.get(user=request.user)
    orders = ProductOrder.objects.filter(customer=customer.id, order_delivered=False)
    context = {
        'title':title,
        'customer':customer,
        'orders':orders,
    }
    return render(request, "view_orders.html", context)


def pick_order(request):
    title = 'Pick Orders'
    employee = Employee.objects.get(user=request.user)
    orders = ProductOrder.objects.filter(warehouse=employee.warehouse)
    products = []
    for i in range(len(orders)):
        products.append(Product_items_details.objects.filter(order_id=orders[i]))
    if orders.exists():
        context = {
        'title':title,
        'employee':employee,
        'orders':orders,
        'products':products,
    }
    else:
        messages.warning(request, "No Orders")
    context = {
        'title':title,
        'employee':employee,
        'orders':orders,
        'products':products,
    }
    return render(request, 'pick_order.html', context)


def total_orders(request):
    orders = ProductOrder.objects.all()
    filt = SearchOrders(request.POST, queryset=orders)
    context = {
        'title':"Total Orders",
        'orders':orders,
        'filter':filt,
    }
    return render(request, 'porders.html', context)


def total_customers(request):
    title = "Customers"
    customers = Customers.objects.all()
    filt = SearchCustomers(request.GET, queryset=customers)
    context = {
        'title':title,
        'customers':customers,
        'filter':filt,
    }
    return render(request, 'total_customers.html', context)


def employees(request):
    title = "Employees"
    employees = Employee.objects.all()
    filt = SearchEmployee(request.GET, queryset=employees)
    context = {
        'title':title,
        'filter':filt,
    }
    return render(request, "employees.html", context)