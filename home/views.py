import json
from unicodedata import category

from django.contrib.auth import logout, authenticate, login

from .forms import SearchForm, SignUpForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

# Create your views here.
from home.models import Setting, ContactFormMessage, ContactFormu
from product.models import Product, Category, Images, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()[:10]
    category = Category.objects.all()
    lastproducts = Product.objects.all().order_by('-id')[:10]


    context = {'setting':setting,
               'category':category,
               'page': 'home',
               'sliderdata':sliderdata,
               'lastproducts': lastproducts,
               }
    return render(request, 'index.html', context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting':setting,
               'category':category,
               'page': 'hakkimizda'}
    return render(request, 'hakkimizda.html', context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting':setting,'page': 'referanslar','category':category}
    return render(request, 'referanslar.html', context)

def iletisim(request):

    if request.method == 'POST':
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesajınız başarı ile gönderilmiştir.")
            return HttpResponseRedirect ('/iletisim')

    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    category = Category.objects.all()
    context = {'setting': setting,'form': form,'category':category}
    return render(request, 'iletisim.html', context)

def category_products(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    products = Product.objects.filter(category_id=id)
    context = {'products':products,
               'category':category,
               'categorydata':categorydata
               }
    return render(request,'products.html',context)

def product_detail(request,id,slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images =Images.objects.filter(product_id=id)
    comments =  Comment.objects.filter(product_id=id,status='True')
    context = {'product':product,
               'category': category,
               'images': images,
               'comments':comments,

               }
    return render(request,'product_detail.html',context)

def product_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category= Category.objects.all()
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']

            if catid==0:
               products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)
            context = {
                'products': products,
                'category': category,
                'query': query
            }

            return render(request, 'products_search.html', context)

        return HttpResponseRedirect('/')

def product_search_auto(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    product = Product.objects.filter(title__icontains=q)
    results = []
    for rs in product:
      product_json = {}
      product_json = rs.title
      results.append(product_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username= request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Giriş Hatası! Kullanıcı adı veya şifre yanlış ")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {
        'category': category,
    }

    return render(request, 'login.html', context)



def signup_view(request):
    if request.method == 'POST':
          form=SignUpForm(request.POST)
          if form.is_valid():
              form.save()
              username = form.cleaned_data.get('username')
              password = form.cleaned_data.get('password1')
              user = authenticate(username=username,password=password)
              login(request, user)
              return HttpResponseRedirect('/')




    form = SignUpForm()
    category = Category.objects.all()
    context = {
        'category': category,
        'form' : form,
    }

    return render(request, 'signup.html', context)

