from django import forms
from .models import *



#class AddProductForm(forms.ModelForm):
#   class Meta:
#       model = Products
#       field = ['product_name', 'product_brand', 'product_category']

class ReceiveProductForm(forms.ModelForm):
    class Meta:
        model = Product_items_details
        fields = ['product_item_name', 'purchased_from', 'purchased_price', 'selling_price', 'product_in', 'rack_name']
     
    #def __init__(self, *args, **kwargs):
     #  super().__init__(*args, **kwargs)
     #  self.fields['rack_name'].queryset = Rack.objects.none()

      # if 'product_in' in self.data:
            #try:
             # product_in = int(self.data.get('product_in'))
             # self.fields['rack_name'].queryset = Rack.objects.filter(rack_warehouse_id=product_in).order_by('rack_name')
           # except (ValueError, TypeError):
             # pass  # invalid input from the client; ignore and fallback to empty City queryset
      # elif self.instance.pk:
           #self.fields['rack_name'].queryset = self.instance.product_in.rack_name_set.order_by('rack_name')
    


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


class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'



