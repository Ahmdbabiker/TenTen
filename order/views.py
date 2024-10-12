from django.shortcuts import render , redirect
from .models import *
from cart.cart import Cart
from django.contrib import messages



def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.total()

        amount_paid = totals

        
        if request.user.is_authenticated:
            user = request.user
            user_data = request.session.get("user_data")
          
            shiping_Address = f"{user_data['address']} \n"
            phone = user_data.get('phoneno')
            pickk = user_data.get('pickup')
            if pickk == "yes":
                picked = True
            else:
                picked = False
            create_order = Order.objects.create(
                user = user , shipping_address = shiping_Address , 
                amount_paid = amount_paid
                ,phone_number = phone , pickup = picked )
           
                

            order_id = create_order.id

            order_id_session = request.session["order_no"] = order_id

            for product in cart_products():
				# Get product ID
                product_id = product.id
				# Get product price
                
                price = product.price


				# Get quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
						# Create order item

                        quantity = value['quantity'] if isinstance(value, dict) else value

                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=quantity, price=price)
                        create_order_item.save()
                    
                        product = Product.objects.get(id = product_id)
                        product.no_of_buying += quantity
                        product.save()

			# Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
            messages.success(request, "تم تأكيد الطلب")
            return redirect('order_done')

        else :
             
            user_data = request.session.get("unknown_user")
           
            dict_user_data = user_data.get("address")
            phone = user_data.get("phone_no")
            unknown_user_name = user_data.get("name")

            create_order = Order.objects.create(
            shipping_address =  dict_user_data ,  amount_paid = amount_paid ,
            phone_number = phone , unknown_user =unknown_user_name )

            order_id = create_order.pk

            order_id_session = request.session["order_no"] = order_id


            for product in cart_products():
				# Get product ID
                product_id = product.id
				# Get product price
              
                price = product.price

				# Get quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
						# Create order item
                        quantity = value['quantity'] if isinstance(value, dict) else value
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=quantity, price=price)
                        create_order_item.save()

			# Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
				    # Delete the key
                    del request.session[key]

                messages.success(request, " تم الطلب")
                return redirect('order_done')
    else:
        messages.success(request, "تم رفض الطلب ")
        return redirect('home')
