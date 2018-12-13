import json
import urllib
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.conf import settings

def register(request):
    form=RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        ''' End reCAPTCHA validation '''

        if result['success']:
            newUser = User(username = username)
            newUser.set_password(password)
            newUser.save()
            login(request, newUser)
            messages.success(request,"Kayıt İşlemi Tamamlanmıştır...")
            return redirect("index")
        else:
            messages.info(request,"Geçersiz Doğrulama...Lütfen tekrar deneyin...")
    context = {
        "form" : form
    }
    return render(request, "register.html",context)

def loginUser(request):
    form=LoginForm(request.POST or None)
    
    context = {
        "form" : form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username, password = password)
        if  user is None:
            messages.info(request,"Kullanıcı Adı veya Şifreniz Hatalı!")
            return render(request,"login.html",context)
        messages.success(request,"Başarıyla Giriş Yaptınız...")
        login(request,user)
        return redirect("index")
    return render(request, "login.html", context)

def logoutUser(request):
    logout(request)
    messages.info(request,"Başarıyla Çıkış Yaptınız...")
    return redirect("index")