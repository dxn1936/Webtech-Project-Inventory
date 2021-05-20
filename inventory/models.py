from django.db import models

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)

	def __str__(self):
		return self.name


class Warehouse(models.Model):
	warehouse_name = models.CharField(max_length=50, blank=True, null=True)
	warehouse_address = models.CharField(max_length=50, blank=True, null=True)

	def __str__(self):
		return self.warehouse_name


class Products(models.Model):
	product_name = models.CharField(max_length=50, blank=True, null=True)
	product_brand = models.CharField(max_length=50, blank=True, null=True)
	product_category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)

	def __str__(self):
		return self.product_name



class Product_items_details(models.Model):
	product_item_name = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True)
	purchased_from = models.CharField(max_length=50, blank=True, null=True)
	purchased_price = models.IntegerField(default='0', blank=True, null=True)
	selling_price = models.IntegerField(default='0', blank=True, null=True)
	product_in = models.ForeignKey(Warehouse, on_delete=models.CASCADE, blank=True)
	product_sold = models.BooleanField(default=0)
	sold_to = models.CharField(max_length=50, blank=True, null=True, default=None)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return str(self.product_item_name)+" "+self.purchased_from+" "+str(self.purchased_price)+" "+str(self.product_in)

