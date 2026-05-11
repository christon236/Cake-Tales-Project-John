from django.db import models

from cakes.models import BaseClass

# Create your models here.

class PaymentStatusChoices(models.TextChoices):

    SUCCESS = 'Success','Success'

    PENDING = 'Pending','Pending'

    FAILED = 'Failed','Failed'



class Payment(BaseClass):

    order = models.OneToOneField('cakes.order',on_delete=models.CASCADE)

    amount = models.FloatField()

    status = models.CharField(max_length=15,choices=PaymentStatusChoices.choices,default=PaymentStatusChoices.PENDING)

    paid_at = models.DateTimeField(null=True,blank=True)

    class Meta:

        verbose_name = 'Payments'

        verbose_name_plural = 'Payments'

    def __str__(self):

        return f'{self.order.user.username}-{self.order.order_id} Payment'
    

class Transaction(BaseClass):

    payment = models.ForeignKey('Payment',on_delete=models.CASCADE)

    amount = models.FloatField()

    status = models.CharField(max_length=15,choices=PaymentStatusChoices.choices,default=PaymentStatusChoices.PENDING)

    rzp_order_id = models.SlugField()

    transaction_at = models.DateTimeField(null=True,blank=True)

    rzp_payment_id = models.SlugField(null=True,blank=True)

    rzp_signature = models.TextField(null=True,blank=True)

    class Meta:

        verbose_name = 'Transactions'

        verbose_name_plural = 'Transactions'

    def __str__(self):

        return f'{self.payment.order.user.username}-{self.payment.order.order_id}-{self.rzp_order_id} Transaction'