from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product_items_details
from .forms import ReceiveProductForm
from django.contrib import messages

# Create your views here.

#@login_required
def home(request):
	title = 'Welcome: This is the Home Page'
	form = 'This is the form variable'
	context = {
		"title": title,
		"test": form,
	}
	return render(request, "home.html",context)

def receive_products(request):
	title = 'RECEIVE ITEMS'
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
