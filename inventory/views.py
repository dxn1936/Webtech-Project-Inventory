from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product_items_details, Products
from .forms import ReceiveProductForm, ProductSearchForm, SearchProductsForm
from django.contrib import messages
from .filters import SearchFilter, SearchProduct


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
		return redirect('/list_products')
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


def dashboard(request):
	product_details = Product_items_details.objects.all()
	total = 0
	for i in product_details:
		total += i.selling_price - i.purchased_price 
	context = {
		'field': total
	}
	return render(request, 'dashboard.html', context)


def sell_products(request):
	title = 'List Of Products'
	products = Products.objects.all()
	filt = SearchProduct(request.GET, queryset=products)
	form = SearchProductsForm(request.GET or None)
	context = {
		'title': title,
		'products': products,
		'filter': filt,
		'form': form
	}
	return render(request, 'sell_products.html', context)

def sell_qty(request,pk):
	all_items = Product_items_details.objects.get(id=int(pk)-1)
	context = {
		'items': all_items
	}
	return render(request, 'sell_qty.html', context)
