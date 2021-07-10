from django.http import HttpResponse
from django.shortcuts import redirect
from .models import *

def authenticate_user(view_function):
	def wrapper(request, *args, **kwargs):
		#cust = Customers.objects.get(user=request.user.id)
		#print(cust.state)
		if request.user.is_superuser:
			return view_function(request, *args, **kwargs)
		elif request.user.is_staff:
			employee = Employee.objects.get(user=request.user)
			employee_designation = Employee.objects.get(user=request.user).designation
			if employee_designation == 'pick_order':
				return redirect("/pick_order")
		else:
			return redirect("place_orders")

	return wrapper


def authenticate_superuser(view_function):
	def container(request, *args, **kwargs):
		if request.user.is_superuser:
			return view_function(request, *args, **kwargs)
		else:
			return redirect("pick_order")
	return container



def is_superuser(view_function):
	def con(request, *args, **kwargs):
		if request.user.is_superuser:
			return redirect('total_orders')
		else:
			return view_function(request, *args, **kwargs)
	return con