from django.db import models

# Create your models here.


class Category(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)

	def __str__(self):
		return self.name

class Suppliers(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	address = models.CharField(max_length=50, blank=True, null=True)

	def __str__(self):
		return self.name

class Customers(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	address = models.CharField(max_length=50, blank=True, null=True)

	def __str__(self):
		return self.name

customers = []
cust = Customers.objects.all()
for i in range(len(cust)):
	customers.append((cust[i].name,cust[i].name),)

class Warehouse(models.Model):
	warehouse_name = models.CharField(max_length=50, blank=True, null=True)
	warehouse_address = models.CharField(max_length=50, blank=True, null=True)

	def __str__(self):
		return self.warehouse_name


class Rack(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, blank=True)
	capacity = models.IntegerField(default='0', blank=True, null=True)

	def __str__(self):
		return self.name


class Products(models.Model):
	product_name = models.CharField(max_length=50, blank=True, null=True)
	product_brand = models.CharField(max_length=50, blank=True, null=True)
	product_category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
	product_quantity = models.IntegerField(default='0', blank=True, null=True)
	product_reorder = models.IntegerField(default='0', blank=True, null=True)

	def __str__(self):
		return self.product_name


class Product_items_details(models.Model):
	product_item_name = models.ForeignKey(Products, on_delete=models.CASCADE, blank=False)
	purchased_from = models.ForeignKey(Suppliers, on_delete=models.CASCADE, blank=False)
	purchased_price = models.IntegerField(default='0', blank=True, null=True)
	selling_price = models.IntegerField(default='0', blank=True, null=True)
	product_in = models.ForeignKey(Warehouse, on_delete=models.CASCADE, blank=False)
	product_sold = models.BooleanField(default=0)
	sold_to = models.CharField(max_length=50, blank=True, null=True, choices=customers)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return str(self.product_item_name)


class Product_Rack(models.Model):
	product = models.ForeignKey(Product_items_details, on_delete=models.CASCADE, blank=True)
	rack = models.ForeignKey(Rack, on_delete=models.CASCADE, blank=True)

	def __str__(self):
		return str(self.product) + str(self.rack)


