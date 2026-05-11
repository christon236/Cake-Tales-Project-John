from django.shortcuts import render,redirect

# Create your views here.

from django.views import View

from  . import models

from .models import Cake,WishList,Cart,Order,DeliveryAddress

from .forms import AddCakeForm

from django.db.models import Q

from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from authentication.permissions import allowed_permission_roles

from cake_tales.utilis import generate_order_id

from payment.models import Payment





class HomeView(View):

    template = 'cakes/home.html'

    def get(self,request,*args,**kwargs):

        query = request.GET.get('query')

        cakes = Cake.objects.filter(active_status=True)

        wedding_cakes = cakes.filter(category__name = 'Wedding cakes')

        birthday_cakes = cakes.filter(category__name = 'Birthday cakes')

        plum_cakes = cakes.filter(category__name = 'Plum cakes')

        cup_cakes = cakes.filter(category__name = 'Cup cakes')

        data = {'wedding_cakes':wedding_cakes,'birthday_cakes':birthday_cakes,'plum_cakes':plum_cakes,'cup_cakes':cup_cakes}

        if query :

            search_results = cakes.filter(Q(name__icontains=query) | 
                                         Q(description__icontains=query)|
                                         Q(category__name__icontains=query)|
                                         Q(flavour__name__icontains=query)|
                                         Q(shape__name__icontains=query)|
                                         Q(weight__name__icontains=query)
                                         )
            
            data['search_results'] = search_results

            data['query'] = query
            


        return render(request,self.template,context=data)


# @method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(allowed_permission_roles(['Admin']),name='dispatch')
class AddACakeView(View):

    template = 'cakes/add-cake.html'

    form_class = AddCakeForm


    def get(self,request,*args,**kwargs):

        form = self.form_class()

        # data = {'categories':models.CategoryChoices,'flavours':models.FlavourChoices,'shapes':models.ShapeChoices,'weights':models.WeightChoices,'form':form}
        data = {'form':form}

        return render(request,self.template,context=data)
    
    def post(self,request,*args,**kwargs):

        # name = request.POST.get('name')

        # description = request.POST.get('description')

        # photo = request.FILES.get('photo')

        # category = request.POST.get('category')

        # flavour = request.POST.get('flavour')

        # shape = request.POST.get('shape')

        # weight = request.POST.get('weight')

        # egg_added = request.POST.get('egg_added')

        # is_available = request.POST.get('is_available')

        # price = request.POST.get('price')

        # cake = Cake.objects.create(name=name,description=description,photo=photo,
        #                                   category=category,flavour=flavour,shape=shape,weight=weight,
        #                                   egg_added=egg_added,is_available=is_available,price=price)

        form = self.form_class(request.POST,request.FILES)

        if form.is_valid():

            form.save()

            return redirect('home')

        data = {'form':form}

        return render(request,self.template,context=data)
    
class CakeDetailsView(View):

    template = 'cakes/cake-details.html'

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        cake = Cake.objects.get(uuid=uuid)

        data = {'cake':cake}

        return render(request,self.template,context=data)
    
@method_decorator(allowed_permission_roles(['Admin']),name='dispatch')
class CakeEditView(View):

    template = 'cakes/cake-edit.html'

    form_class = AddCakeForm


    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        cake = Cake.objects.get(uuid=uuid)

        form = self.form_class(instance=cake)

        data = {'cake':cake,'form':form}

        return render(request,self.template,context=data)
    
    def post(self,request,*args,**kwargs):

        
        uuid = kwargs.get('uuid')

        cake = Cake.objects.get(uuid=uuid)

        form = self.form_class(request.POST,request.FILES,instance=cake)

        if form.is_valid():

            form.save()

            return redirect('cake-details',uuid=cake.uuid)
        
        data = {'form':form}

        return render(request,self.template,context=data)


@method_decorator(allowed_permission_roles(['Admin']),name='dispatch')    
class CakeDeleteView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        cake = Cake.objects.get(uuid=uuid)

        cake.active_status = False

        cake.save()

        return redirect('home')
    

@method_decorator(allowed_permission_roles(['User']),name='dispatch')    
class AddtoWishList(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        user = request.user

        cake = Cake.objects.get(uuid=uuid)

        wishlist,_ = WishList.objects.get_or_create(user=user)

        wishlist.cakes.add(cake)

        return redirect('home')

@method_decorator(allowed_permission_roles(['User']),name='dispatch')    
class RemovefromWishList(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        user = request.user

        cake = Cake.objects.get(uuid=uuid)

        wishlist = WishList.objects.get(user=user)

        wishlist.cakes.remove(cake)

        return redirect('home')
    
@method_decorator(allowed_permission_roles(['User']),name='dispatch')    
class WishListView(View):

    template = 'cakes/wishlist.html'

    def get(self,request,*args,**kwargs):

        return render(request,self.template)

@method_decorator(allowed_permission_roles(['User']),name='dispatch')    
class AddtoCart(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        user = request.user

        cake = Cake.objects.get(uuid=uuid)

        cart,_ = Cart.objects.get_or_create(user=user)

        cart.cakes.add(cake)

        return redirect('home')
    

@method_decorator(allowed_permission_roles(['User']),name='dispatch')    
class RemovefromCart(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        user = request.user

        cake = Cake.objects.get(uuid=uuid)

        cart = Cart.objects.get(user=user)

        cart.cakes.remove(cake)

        return redirect('home')
    
class CheckoutView(View):

    template = 'cakes/checkout.html'

    def get(self,request,*args,**kwargs):

        user = request.user

        order_id = generate_order_id()

        print(order_id)

        cakes_ids = user.cart.cakes.values_list('id',flat=True)

        cakes = user.cart.cakes.all()

        total_price = user.cart.get_total

        orders = Order.objects.filter(user=user,total_price=total_price,cakes__in=cakes_ids,order_placed=False)

        print(orders)

        if orders.exists() :

            order = orders.distinct().first()

            print(order)

        else :

            order = Order.objects.create(user=user,order_id=order_id,total_price=total_price)

            order.cakes.add(*cakes)

        data = {'order':order}


        return render(request,self.template,context=data)
    
class OrderPlacedView(View):

    def post(self,request,*args,**kwargs):

        order_uuid = kwargs.get('uuid')

        address_uuid = request.POST.get('address')

        payment_method = request.POST.get('payment')

        address = DeliveryAddress.objects.get(uuid=address_uuid)

        order = Order.objects.get(user=request.user,uuid=order_uuid)

        order.delivery_address = address

        order.payment_method = payment_method

        order.save()

        payment = Payment.objects.filter(order=order)

        if payment.exists():

            payment = payment.first()

        else :

            payment = Payment.objects.create(order=order,amount=order.total_price)

        if payment_method == 'Online':

            return redirect('razorpay',uuid=payment.uuid)

        else : 

            return redirect('home')


@method_decorator(allowed_permission_roles(['User']),name='dispatch')    
class OrdersView(View):

    template = 'cakes/orders.html'

    def get(self,request,*args,**kwargs):
       
       orders = Order.objects.filter(user=request.user)

       data = {'orders':orders}

       return render(request,self.template,context=data)



class OrderDetailsView(View):

    template = 'cakes/order-details.html'

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        user = request.user

        order = Order.objects.get(uuid=uuid)

        data = {'order':order}

        return render(request,self.template,context=data)