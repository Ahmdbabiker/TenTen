from django.db import models
from django.contrib.auth.models import User
from core.models import *
# Create your models here.


# Create Order Model
class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	shipping_address = models.TextField(max_length=15000)
	amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
	date_ordered = models.DateTimeField(auto_now_add=True)	
	phone_number = models.IntegerField(null=True , blank=True)
	unknown_user = models.CharField(null=True , max_length=50 , blank=True)
	pickup = models.BooleanField(default=False , null=True)
	is_new = models.BooleanField(default=True , null=True)  # Indicates if the order is new

	def __str__(self):
		return f'Order - {str(self.id)}'

	def order_items(self):
		return  OrderItem.objects.filter(order__id = self.id)

# Create Order Items Model
class OrderItem(models.Model):
	# Foreign Keys
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	quantity = models.PositiveBigIntegerField(default=1)
	price = models.DecimalField(max_digits=7, decimal_places=2)


	def __str__(self):
		return f'Order Item - {str(self.id)}'
