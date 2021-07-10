import django_filters
from .models import *

class SearchFilter(django_filters.FilterSet):
	class Meta:
		model = Product_items_details
		fields = ['product_item_name', 'purchased_from', 'purchased_price', 'product_in', 'room', 'reserved', 'order_id','product_sold', 'sold_to']


class SearchProduct(django_filters.FilterSet):
	class Meta:
		model = Products
		fields = ['product_name', 'product_brand']

class SearchSupplier(django_filters.FilterSet):
	class Meta:
		model = Suppliers
		fields = ['name']

class SearchSold(django_filters.FilterSet):
	class Meta:
		model = Product_items_details
		fields = ['product_item_name','product_in','purchased_from']



class SearchCustomers(django_filters.FilterSet):
	class Meta:
		model = Customers
		fields = ['name', 'state', 'city']

class SearchEmployee(django_filters.FilterSet):
	class Meta:
		model = Employee
		fields = ['warehouse','salary','designation']

class SearchOrders(django_filters.FilterSet):
	class Mata:
		model = ProductOrder
		fields = ['quantity','customer_id']
