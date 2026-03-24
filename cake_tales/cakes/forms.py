from django import forms

from .models import Cake

class AddCakeForm(forms.ModelForm):

    class Meta :

        model = Cake

        # fields or exclude

        # fields --- for include 
        # exclude ---- for exclude

        # feilds =['name','description']

        # fields = '__all__'

        exclude = ['uuid','active_status']
        
        widgets = {'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Cake Name'}),
                   
                   'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Enter Cake Description','rows':'3'}),
                   
                   'photo':forms.FileInput(attrs={'class':'form-control'}),
                   
                   'category':forms.Select(attrs={'class':'form-select'}),

                   'flavour':forms.Select(attrs={'class':'form-select'}),
        
                   'shape':forms.Select(attrs={'class':'form-select'}),

                   'weight':forms.Select(attrs={'class':'form-select'}),

                   'egg_added':forms.RadioSelect(choices=[(True,'Yes'),(False,'No')],attrs={'class':'form-check-input','name':'egg_added'}),

                   'is_available':forms.RadioSelect(choices=[(True,'Yes'),(False,'No')],attrs={'class':'form-check-input','name':'is_available'}),

                   'price':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Price'})


                   }
        
    def clean(self):

        validated_data = super().clean()

        price = validated_data.get('price')

        if price < 0:

            self.add_error('price','price must be positive number')
            
        return super().clean()