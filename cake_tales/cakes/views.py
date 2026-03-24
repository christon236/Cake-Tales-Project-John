from django.shortcuts import render,redirect

# Create your views here.

from django.views import View

from  . import models

from .models import Cake

from .forms import AddCakeForm

from django.db.models import Q



class HomeView(View):

    template = 'cakes/home.html'

    def get(self,request,*args,**kwargs):

        quary = request.GET.get('quary')

        cakes = Cake.objects.filter(active_status=True)

        wedding_cakes = cakes.filter(category__name = 'Wedding cakes')

        birthday_cakes = cakes.filter(category__name = 'Birthday cakes')

        plum_cakes = cakes.filter(category__name = 'Plum cakes')

        cup_cakes = cakes.filter(category__name = 'Cup cakes')

        data = {'wedding_cakes':wedding_cakes,'birthday_cakes':birthday_cakes,'plum_cakes':plum_cakes,'cup_cakes':cup_cakes}

        if quary :

            search_results = cakes.filter(Q(name__icontains=quary) | 
                                         Q(description__icontains=quary)|
                                         Q(category__name__icontains=quary)|
                                         Q(flavour__name__icontains=quary)|
                                         Q(shape__name__icontains=quary)|
                                         Q(weight__name__icontains=quary)
                                         )
            
            data['search_results'] = search_results
            


        return render(request,self.template,context=data)
    
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
    
class CakeDeleteView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        cake = Cake.objects.get(uuid=uuid)

        cake.active_status = False

        cake.save()

        return redirect('home')