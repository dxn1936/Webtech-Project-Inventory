from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product_items_details, Products
from .forms import ReceiveProductForm, ProductSearchForm, SearchProductsForm, UpdateSoldForm
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
	title = 'List of Products'
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