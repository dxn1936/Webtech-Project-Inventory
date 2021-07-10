from django.db import models
from django.contrib.auth.models import User
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
	user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, blank=True)
	name = models.CharField(max_length=50, blank=False, null=True)
	state = models.CharField(max_length=50, blank=False, null=True)
	city = models.CharField(max_length=50, blank=False, null=True)
	pincode = models.IntegerField(blank=True, null=True)
	address = models.CharField(max_length=50, blank=False, null=True)
	payment_due = models.DecimalField(default='0', max_digits=19, decimal_places=3)
	total_order_amount = models.DecimalField(default='0', max_digits=19, decimal_places=3)
	username = models.CharField(max_length=50, blank=False, null=True)
	password = models.CharField(max_length=50, blank=True, null=True)

	def __str__(self):
		return self.name

class Warehouse(models.Model):
	warehouse_name = models.CharField(max_length=50, blank=True, null=True)
	warehouse_address = models.CharField(max_length=50, blank=True, null=True)

	def __str__(self):
		return self.warehouse_name

class Employee(models.Model):
	user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, blank=True)
	name = models.CharField(max_length=50, blank=False, null=True)
	salary = models.IntegerField(blank=True, null=True)
	designation = models.CharField(max_length=50, blank=True, null=True)
	warehouse = models.ForeignKey(Warehouse, null=True, on_delete=models.CASCADE, blank=True)

	def __str__(self):
		return self.name


class Rack(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, blank=True)
	total_storage_vol = models.DecimalField(default='0', max_digits=19, decimal_places=2)
	available_storage_vol = models.DecimalField(default='0', max_digits=19, decimal_places=2)

	def __str__(self):
		return self.name


class Products(models.Model):
	product_name = models.CharField(max_length=50, blank=True, null=True)
	product_brand = models.CharField(max_length=50, blank=True, null=True)
	product_category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
	product_quantity = models.IntegerField(default='0', blank=True, null=True)
	product_reorder = models.IntegerField(default='0', blank=True, null=True)
	product_length_cm = models.DecimalField(default='0', max_digits=19, decimal_places=2)
	product_width_cm = models.DecimalField(default='0', max_digits=19, decimal_places=2)
	product_height_cm = models.DecimalField(default='0', max_digits=19, decimal_places=2)
	product_weight_g = models.DecimalField(default='0', max_digits=19, decimal_places=2)

	def __str__(self):
		return self.product_name


class ProductOrder(models.Model):
	customer = models.ForeignKey(Customers, on_delete=models.CASCADE, blank=True)
	warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, blank=True, null=True)
	product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True)
	quantity = models.IntegerField(default='0', blank=True, null=True)
	order_cancelled = models.BooleanField(default=0)
	order_delivered = models.BooleanField(default=0)
	order_total_amt = models.DecimalField(default='0', max_digits=19, decimal_places=2)
	order_paid = models.BooleanField(default=0)

	def __str__(self):
		return str(self.id)


class Product_items_details(models.Model):
	product_item_name = models.ForeignKey(Products, on_delete=models.CASCADE, blank=False)
	purchased_from = models.ForeignKey(Suppliers, on_delete=models.CASCADE, blank=False)
	purchased_price = models.IntegerField(default='0', blank=True, null=True)
	selling_price = models.IntegerField(default='0', blank=True, null=True)
	product_in = models.ForeignKey(Warehouse, on_delete=models.CASCADE, blank=False)
	room = models.ForeignKey(Rack, on_delete=models.CASCADE, blank=True)
	reserved = models.BooleanField(default=0)
	order_id = models.ForeignKey(ProductOrder, on_delete=models.CASCADE, blank=True, null=True)
	product_sold = models.BooleanField(default=0)
	sold_to = models.ForeignKey(Customers, on_delete=models.CASCADE, blank=True, null=True)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return str(self.product_item_name)


class Measurements(models.Model):
	location = models.CharField(max_length=50, blank=True, null=True)
	destination = models.CharField(max_length=50, blank=True, null=True)
	distance = models.DecimalField(default='0', max_digits=19, decimal_places=2)






