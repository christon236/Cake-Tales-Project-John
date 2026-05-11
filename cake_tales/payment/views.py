from django.shortcuts import render,redirect

from django.views import View

from .models import Payment,Transaction

import razorpay

from decouple import config

from django.utils import timezone

from django.contrib import messages


# Create your views here.


class RazorpayView(View):

    template = 'payment/razorpay.html'

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        payment_obj = Payment.objects.get(uuid=uuid)

        client = razorpay.Client(auth=(config('RZP_CLIENT_ID'),config('RZP_CLIENT_SECRET')))

        data = { "amount": payment_obj.amount*100, "currency": "INR", "receipt": "order_rcptid_11" }

        payment = client.order.create(data=data)   # // Amount is in currency subunits.

        rzp_order_id = payment.get('id')

        print(rzp_order_id)


        transaction = Transaction.objects.create(payment=payment_obj,amount=payment_obj.amount,rzp_order_id=rzp_order_id)

        data = {'order_id':rzp_order_id,'amount':payment.get('amount'),'RZP_CLIENT_ID':config('RZP_CLIENT_ID')}

        return render(request,self.template,context=data)
    

class PaymentVerifyView(View):

    def post(self,request,*args,**kwargs):

        rzp_order_id = request.POST.get('razorpay_order_id')

        rzp_payment_id = request.POST.get('razorpay_payment_id')

        rzp_signature = request.POST.get('razorpay_signature')

        transaction = Transaction.objects.get(rzp_order_id=rzp_order_id)

        transaction.rzp_payment_id = rzp_payment_id

        transaction.rzp_signature = rzp_signature

        transaction.transaction_at = timezone.now()

        
        client = razorpay.Client(auth=(config('RZP_CLIENT_ID'),config('RZP_CLIENT_SECRET')))

        paid = client.utility.verify_payment_signature({
                            'razorpay_order_id': rzp_order_id,
                            'razorpay_payment_id': rzp_payment_id,
                            'razorpay_signature': rzp_signature
                                                    })
        
        if paid :

            transaction.status = 'Success'

            transaction.payment.status = 'Success'

            transaction.payment.paid_at = timezone.now()

            transaction.payment.save()

            transaction.save()

            transaction.payment.order.order_placed = True

            transaction.payment.order.save()

            request.user.cart.cakes.clear()

            messages.success (request,'Order placed successfully')

            return redirect('home')
        
        else :

            transaction.status = 'Failed'

            transaction.save()

            messages.error(request,'Payment failed')

            return redirect('razorpay')