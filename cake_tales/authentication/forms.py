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
    

class OTPForm(forms.Form):

    otp = forms.CharField(max_length=4,widget=forms.TextInput(attrs={'placeholder':'Enter OTP','required':'required','class':'form-control'}))

    def clean(self):

        otp = super().clean().get('otp')

        if len(otp) < 4 :
      
            self.add_error('otp','otp must be 4 digits')

        return super().clean()
    

class SetPasswordForm(forms.Form):

    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password','required':'required','class':'form-control'}))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm password','required':'required','class':'form-control'}))

    def clean(self):

        password = super().clean().get('password')

        confirm_password = super().clean().get('confirm_password')

        if password != confirm_password :

            self.add_error('confirm_password','password mismatch')

        return super().clean()
    

class ForgotPasswordForm(forms.Form):

    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder':'Enter registered email','required':'required','class':'form-control'}))

 
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

        if not Profile.objects.filter(email=email).exists():

            self.add_error('email','unregistered email address')

        return super().clean()