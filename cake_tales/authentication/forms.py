from django import forms

from .models import Profile

class LoginForm(forms.Form):

    username = forms.CharField(widget=forms.EmailInput(attrs={'placeholder':'Enter email','required':'required','class':'form-control'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter password','required':'required','class':'form-control'}))

    def clean(self):

        domain_list = [
            "gmail.com",
            "yahoo.com",
            "outlook.com",
            "hotmail.com",
            "icloud.com",
            "zoho.com",
            "mailinator.com"
        ]

        username = super().clean().get('username')

        _,domain = username.split('@')

        if domain not in domain_list:

            self.add_error('username','invalid email domain')



        return super().clean()
    
class RegisterForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = ['first_name','email']

        widgets = {

                'first_name':forms.TextInput(attrs={'class':'form-control','required':'required','placeholder':'Enter Name'}),

                'email':forms.EmailInput(attrs={'class':'form-control','required':'required','placeholder':'Enter Email'}),
        }

    
    def clean(self):

        domain_list = [
            "gmail.com",
            "yahoo.com",
            "outlook.com",
            "hotmail.com",
            "icloud.com",
            "zoho.com",
            "mailinator.com"
        ]

        email = super().clean().get('email')

        _,domain = email.split('@')

        if domain not in domain_list:

            self.add_error('email','invalid email domain')

        if Profile.objects.filter(email=email).exists():

            self.add_error('email','This email already registed')



        return super().clean()