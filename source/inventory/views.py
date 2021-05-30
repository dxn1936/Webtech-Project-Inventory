from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib import messages
from .filters import SearchFilter, SearchProduct
import csv,datetime
from django.http import HttpResponse
from django.db.models import Count
from django.db.models import Q

#import array as product_arr 
#import array as product_counts


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
        messages.success(request, 'Successfully saved')
        return redirect('/receive_products')
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
    return render(request, "list_products.html",  context)


def dashboard(request):
    product_details = Product_items_details.objects.all()
    product_count = product_details.count()
    product = Products.objects.all()
    details = product.count()
    supplier = Suppliers.objects.all().count()
    sold = Product_items_details.objects.filter(product_sold='1').count()
   # sold = Product_items_details.objects.filter(product_sold='1').count().distinct()
    available = Product_items_details.objects.filter(product_sold='0').count()
    total = 0
   
    customers = Product_items_details.objects.values('sold_to').distinct().count()
    category = Category.objects.all()

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
        'category' : category
    }
    return render(request, 'dashboard.html', context)




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
            messages.success(request, 'Successfully Issued')
            return redirect('/sell_products')
    return render(request, 'issue_product.html', {'title':'ISSUE', 'form':form, 'item_name':item_name, 'category':category, 'supplier': supplier, 'rate':rate, 'warehouse':warehouse})



def export_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=Inventory'+ \
        str(datetime.datetime.now())+'.csv'

    writer=csv.writer(response)
    writer.writerow(['PRODUCT_ITEM_NAME','PURCHASED_FROM','PURCHASED_PRICE','SELLING_PRICE','PRODUCT_IN','PRODUCT_SOLD','SOLD_TO','TIMESTAMP'])
    product=Product_items_details.objects.filter()

    for Stock in product:
            writer.writerow([Stock.product_item_name,Stock.purchased_from,Stock.purchased_price,
                                Stock.selling_price,Stock.product_in,Stock.product_sold,Stock.sold_to,Stock.timestamp])

    return response 

def selproduct_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=Sellproduct'+ \
        str(datetime.datetime.now())+'.csv'

    writer=csv.writer(response)
    writer.writerow(['PRODUCT_NAME','PRODUCT_BRAND','PRODUCT_QUANTITY'])
    product=Products.objects.filter()
    for Stock in product:
            writer.writerow([Stock.product_name,Stock.product_brand,
                                Stock.product_quantity])
    return response 


def load_racks(request):
    warehouse_id = request.GET.get('warehouse_id')
    racks = Rack.objects.filter(rack_warehouse_id=warehouse_id)
 #   rack = Product_items_details.objects.values('rack_name_id').annotate(Count('rack_name_id'))
   # for i in range(len(racks)):
   #  product_details = racks.get(rack_capacity)
    # filters = Q(product_details=rack)

    return render(request, 'dropdown.html', {'racks': racks})
    #print(list(racks.values('id', 'name')))
    #return JsonResponse(list(racks.values('id', 'name')), safe=False)



