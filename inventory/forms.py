from django import forms
from .models import *



#class AddProductForm(forms.ModelForm):
#	class Meta:
#		model = Products
#		field = ['product_name', 'product_brand', 'product_category']

class ReceiveProductForm(forms.ModelForm):
	class Meta:
		model = Product_items_details
		fields = ['product_item_name', 'purchased_from', 'purchased_price', 'selling_price', 'product_in']

