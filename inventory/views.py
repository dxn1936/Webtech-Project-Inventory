from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product_items_details
from .forms import ReceiveProductForm, ProductSearchForm
from django.contrib import messages
from .filters import SearchFilter


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
