from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder

from django.contrib import messages
from django.views import View
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from django.http import JsonResponse , HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from num2words import num2words

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	# messages.error(request, 'Member Type data not found!')
	# messages.success(request, 'One active content already exit.')
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	stockQuantity = data['stockQuantity']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)
	print('stockQuantity:', stockQuantity)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		if orderItem.quantity < int(stockQuantity):
			orderItem.quantity = (orderItem.quantity + 1)
		else:
			messages.error(request, 'Sorry Not enough stock available of this product!')
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		zipcode=data['shipping']['zipcode'],
		)

	global order_id 
	order_id = order.id

	return JsonResponse(order.id, safe=False)

@csrf_exempt
def handlerequest(request):
    return render(request, 'store/ordersuccess.html',{'id':order_id})


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

class GenerateInvoice(View):
    def get(self, request, *args, **kwargs):
        try:
            order_db = Order.objects.get(id = order_id)
        except:
            return HttpResponse("505 Not Found")
        data = {
            'order_id'			: order_db.id,
            'qr_img'			: "static/images/" + str(order_db.qr_code),
            'order'				: order_db,
            'amount'			: order_db.get_cart_total,
            'amount_word'		: num2words(order_db.get_cart_total),
        }
        pdf = render_to_pdf('store/order_invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')