from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import datetime

# Customer table
class Customer(models.Model):
	user    = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name    = models.CharField(max_length=200, null=True)
	phone   = models.CharField(max_length=200, null=True)
	email   = models.CharField(max_length=200)

	def __str__(self):
		return self.name

# Product table
class Product(models.Model):
	code            = models.CharField(max_length=200)
	name            = models.CharField(max_length=200)
	category        = models.CharField(max_length=200)
	price           = models.FloatField()
	stock_quantity  = models.IntegerField(default=0, null=True, blank=True)
	digital         = models.BooleanField(default=False,null=True, blank=True)
	image           = models.ImageField(null=True, blank=True)
	created_date    = models.DateTimeField(default = now )

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

# Order table
class Order(models.Model):
	customer        = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered    = models.DateTimeField(auto_now_add=True)
	complete        = models.BooleanField(default=False)
	transaction_id  = models.CharField(max_length=100, null=True)
	qr_code			= models.ImageField(upload_to='qr', blank=True)
	created_date    = models.DateTimeField(default = now)

	def __str__(self):
		return str(self.id)

	# Automatic QR Code image generate
	def save(self, *args, **kwargs):
		dt_string = str(self.created_date)
		new_dt = dt_string[:19]
		temp_date = datetime.datetime.strptime(new_dt, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
		code_data = "DATE:  " + str(temp_date) + "\n" + "INVOICE NO:  " + str(self.id) + "\n" + "NAME:  " + str(self.customer.name) + "\n" + "PHONE:  " + str(self.customer.phone) + "\n" + "EMAIL:  " + str(self.customer.email)
		if code_data:
			qrcode_img = qrcode.make(code_data)
			canvas = Image.new('RGB', (500, 500), 'white')
			canvas.paste(qrcode_img)
			fname = f'qr_code-{self.transaction_id}.png'
			buffer = BytesIO()
			canvas.save(buffer,'PNG')
			self.qr_code.save(fname, File(buffer), save=False)
			canvas.close()
			super().save(*args, **kwargs)

	# By this model function, we can define, is order shipping is necessary or not. 
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	# By this model function, we can get cart total price.
	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	# By this model function, we can get total quantity of cart items.
	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total

# OrderItem table
class OrderItem(models.Model):
	product     = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order       = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity    = models.IntegerField(default=0, null=True, blank=True)
	date_added  = models.DateTimeField(auto_now_add=True)

	# By this model function, we can get total price after quantity and price multiply.
	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

# ShippingAddress table
class ShippingAddress(models.Model):
	customer    = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order       = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address     = models.CharField(max_length=200, null=False)
	city        = models.CharField(max_length=200, null=False)
	zipcode     = models.CharField(max_length=200, null=False)
	date_added  = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address