from django import forms
from .models import *



#class AddProductForm(forms.ModelForm):
#	class Meta:
#		model = Products
#		field = ['product_name', 'product_brand', 'product_category']

class ReceiveProductForm(forms.ModelForm):
	class Meta:
		model = Product_items_details
		fields = ['product_item_name', 'purchased_from', 'purchased_price', 'selling_price', 'product_in','quantity']
	quantity = forms.IntegerField()

class ProductSearchForm(forms.ModelForm):
	class Meta:
		model = Product_items_details
		fields = ['purchased_from']

class SearchProductsForm(forms.ModelForm):
	class Meta:
		model = Products
		fields = ['product_name']


class UpdateSoldForm(forms.ModelForm):
	class Meta:
		model = Product_items_details
		fields = ['sold_to']

class SearchSupplierForm(forms.ModelForm):
	class Meta:
		model = Suppliers
		fields = ['name']


class SearchSoldForm(forms.ModelForm):
	class Meta:
		model = Product_items_details
		fields = ['product_item_name']

class SearchCustomerForm(forms.ModelForm):
	class Meta:
		model = Customers
		fields = ['name']

class UpdateWarehouseForm(forms.ModelForm):
	class Meta:
		model = Product_items_details
		fields = ['product_in']

