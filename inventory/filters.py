import django_filters
from .models import *

class SearchFilter(django_filters.FilterSet):
	class Meta:
		model = Product_items_details
		fields = ['product_item_name', 'purchased_from', 'purchased_price', 'product_in', 'product_sold', 'sold_to']


class SearchProduct(django_filters.FilterSet):
	class Meta:
		model = Products
		fields = ['product_name']