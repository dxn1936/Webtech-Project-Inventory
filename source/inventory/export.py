from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib import messages
from .filters import SearchFilter, SearchProduct, SearchSupplier, SearchSold, SearchCustomer
import csv,datetime
from django.http import HttpResponse
def stock_csv(request):
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

def supplier_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=suppliers'+ \
        str(datetime.datetime.now())+'.csv'

    writer=csv.writer(response)
    writer.writerow(['SUPPLIER_NAME','ADDRESS'])
    supplier=Suppliers.objects.filter()
    for i in supplier:
            writer.writerow([i.name,i.address])
    return response 

def sold_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=products Sold'+ \
        str(datetime.datetime.now())+'.csv'

    writer=csv.writer(response)
    writer.writerow(['PRODUCT_NAME','PURCHASED_FROM','PURCHASED_PRICE','SELLING_PRICE','WAREHOUSE','SOLD_TO'])
    products= Product_items_details.objects.filter(product_sold=True)
    for i in products:
            writer.writerow([i.product_item_name,i.purchased_from,i.purchased_price,i.selling_price,i.product_in,
                                i.sold_to])
    return response

def customers_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=Customers details'+ \
        str(datetime.datetime.now())+'.csv'

    writer=csv.writer(response)
    writer.writerow(['CUSTOMER NAME','CUSTOMER ADDRESS'])
    Customer=  Customers.objects.all()
    for i in Customer:
            writer.writerow([i.name,i.address])
    return response
