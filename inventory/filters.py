import django_filters
from .models import *

class SearchFilter(django_filters.FilterSet):
	class Meta:
		model = Product_items_details
		fields = ['product_item_name']


