from django.shortcuts import render,redirect

from django.views import View

from .forms import LoginForm,RegisterForm,OTPForm,SetPasswordForm,ForgotPasswordForm

from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.hashers import make_password

from cake_tales.utilis import generate_password,send_email,generate_otp

import threading

from cakes.models import WishList,Cart

from django.db import transaction

from django.contrib import messages

from authentication.models import OTP

from django.utils import timezone

from .models import Profile

# Create your views here.

class LoginView(View):

    template = 'authentication/login.html'

    form_class = LoginForm

    def get(self,request,*args,**kwargs):

        form = self.form_class()

        data = {'form':form}

        return render(request,self.template,context=data)
    
    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)

        data = {'form':form}

        if form.is_valid():

            user = authenticate(**form.cleaned_data)

            if user:

                login(request,user)

                messages.success(request,'successfully logined')

                return redirect('home')
            
            data['msg'] = 'invalid username or password'

        return render(request,self.template,context=data)
    

class LogoutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect('home')


class RegisterView(View):

    template = 'authentication/register.html'

    form_class = RegisterForm

    def get(self,request,*args,**kwargs):

        form = self.form_class()

        data = {'form':form}

        return render(request,self.template,context=data)
    
    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():
           
           with transaction.atomic():


                user = form.save(commit=False)

                email = form.cleaned_data.get('email')

                password = generate_password()

                user.username = email

                user.password = make_password(password)

                user.role = 'User'

                user.save()

                WishList.objects.create(user=user)

                Cart.objects.create(user=user)

           subject = 'Cake Tales | Login Credentials'

           recipient = email

           template = 'emails/login-credentials.html'

           context = {'name':user.first_name,'username':user.username,'password':password}

           thread = threading.Thread(target=send_email,args=(subject,recipient,template,context)) 

           thread.start()

            # send_email(subject,recipient,template,context)

           messages.success(request,'User registered successfully')

           return redirect('login')

        data = {'form':form}

        return render(request,self.template,context=data)
    
class GenerateOTPView(View):

    template = 'authentication/otp.html'

    form_class = OTPForm

    def get(self,request,*args,**kwargs):

        if request.user and request.user.is_authenticated:

            user = request.user

        else :

            email = request.session['email']

            user = Profile.objects.get(username=email)

        otp = generate_otp()

        otp_obj,_ = OTP.objects.get_or_create(user=user)

        otp_obj.otp = otp

        otp_obj.save()

        subject = 'Cake Tales | OTP for Change Password'

        recipient = user.email

        template = 'emails/email-otp.html'

        context = {'name':user.first_name,'otp':otp}

        thread = threading.Thread(target=send_email,args=(subject,recipient,template,context)) 

        thread.start()

        remaining_time = 300

        request.session['otp_time'] = timezone.now().timestamp()

        form = self.form_class()

        data = {'form':form,'remaining_time':remaining_time}

        return render(request,self.template,context=data)
    
    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():

            user_otp = form.cleaned_data.get('otp')

            if request.user and request.user.is_authenticated:

                user = request.user

            else :

                email = request.session['email']

                user = Profile.objects.get(username=email)

            db_otp = user.otp.otp

            otp_time = request.session['otp_time']

            msg = None
            
            if otp_time :

                elapsed_time = timezone.now().timestamp()-otp_time

                if elapsed_time > 300 :

                    msg = 'OTP Expired'

                elif user_otp == db_otp :

                    user.otp.otp_verified = True

                    user.otp.save()

                    messages.success(request,'OTP Verified Successfully')

                    return redirect('set-password')
                
                else :

                    msg = 'Invalid OTP'

                remaining_time = max(0,300-elapsed_time)

        data = {'form':form,'msg':msg}

        return render(request,self.template,context=data)


class SetPasswordView(View):

    template = 'authentication/set-password.html'

    form_class = SetPasswordForm

    def get(self,request,*args,**kwargs):

    
        if request.user and request.user.is_authenticated:

            user = request.user

        else :

            email = request.session['email']

            user = Profile.objects.get(username=email)

        form = self.form_class()

        data = {'form':form}

        if user.otp.otp_verified :

            return render(request,self.template,context=data)
        
        return redirect('generate-otp')
    
    def post(self,request,*args,**kwargs):

        form =self.form_class(request.POST)

        if form.is_valid():

            password = form.cleaned_data.get('password')


            if request.user and request.user.is_authenticated:

                user = request.user

            else :

                email = request.session['email']

                user = Profile.objects.get(username=email)

            user.password = make_password(password)

            user.save()

            user.otp.otp_verified = False

            user.otp.save()

            request.session.clear()

            messages.success(request,'Password Successfully Updated')

            logout(request)

            return redirect('login')

        data = {'form':form}

        return render(request,self.template,context=data)
    

class ForgotPasswordView(View):

    template = 'authentication/forgot-password.html'

    form_class = ForgotPasswordForm

    def get(self,request,*args,**kwargs):

        form = self.form_class()

        data = {'form':form}

        return render(request,self.template,context=data)
    
    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():

            email = form.cleaned_data.get('email')

            request.session['email'] = email

            return redirect('generate-otp')
        
        data = {'form':form}

        return render(request,self.template,context=data)





        







