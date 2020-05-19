import json
from unicodedata import category

from django.contrib.auth import logout, authenticate, login

from user.models import Menu, CImages, Content
from .forms import SearchForm, SignUpForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

# Create your views here.
from home.models import Setting, ContactFormMessage, ContactFormu, UserProfile
from product.models import Product, Category, Comment, Images


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()[:10]
    category = Category.objects.all()
    lastproducts = Product.objects.all().order_by('-id')[:10]
    menu=Menu.objects.all()


    context = {'setting':setting,
               'category':category,
               'page': 'home',
               'sliderdata':sliderdata,
               'lastproducts': lastproducts,
               'menu' : menu
               }
    return render(request, 'index.html', context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    menu = Menu.objects.all()
    context = {'setting':setting,
               'category':category,
               'page': 'hakkimizda',
               'menu' : menu}
    return render(request, 'hakkimizda.html', context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    menu = Menu.objects.all()
    context = {'setting':setting,'page': 'referanslar','category':category, 'menu': menu}
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
    menu = Menu.objects.all()
    context = {'setting': setting,'form': form,'category':category, 'menu': menu}
    return render(request, 'iletisim.html', context)

def category_products(request,id,slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    menu = Menu.objects.all()
    products = Product.objects.filter(category_id=id)
    context = {'products':products,
               'category':category,
               'categorydata':categorydata,
               'menu': menu,
               'setting': setting,
               }
    return render(request,'products.html',context)

def product_detail(request,id,slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    menu = Menu.objects.all()
    product = Product.objects.get(pk=id)
   # profile = UserProfile.objects.get(user_id=product.user_id)
    images = Images.objects.filter(product_id=id)
    comments =  Comment.objects.filter(product_id=id,status='True')
    context = {'product':product,
               'category': category,
               'images': images,
               'comments':comments,
                'menu': menu,
               'setting': setting,
              #  'profile':profile
               }
    return render(request,'product_detail.html',context)

def product_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            setting = Setting.objects.get(pk=1)
            category= Category.objects.all()
            menu = Menu.objects.all()
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']

            if catid==0:
               products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)
            context = {
                'products': products,
                'category': category,
                'query': query,
                'menu': menu,
                'setting': setting,
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
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    menu = Menu.objects.all()
    context = {
        'category': category,
        'menu' : menu,
        'setting': setting,
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

              current_user=request.user
              data=UserProfile()
              data.user_id=current_user.id
              data.image="images/users/user.png"
              data.save()
              messages.success(request, "Kayıt Gerçekleşti!")
              return HttpResponseRedirect('/')
    setting = Setting.objects.get(pk=1)
    form = SignUpForm()
    category = Category.objects.all()
    menu = Menu.objects.all()
    context = {
        'category': category,
        'form' : form,
        'menu': menu,
        'setting': setting,
    }

    return render(request, 'signup.html', context)

def contentdetail(request,id,slug):
    category = Category.objects.all()
    menu= Menu.objects.all()
    setting = Setting.objects.get(pk=1)
    try:
        content = Content.objects.get(pk=id)
        images = CImages.objects.filter(content_id=id)
        context={
            'content':content,
            'category':category,
            'menu ': menu,
            'images':images,
            'setting': setting,
        }
        return render(request,'content_detail.html',context)
    except:
        messages.warning(request,"İlgili içerik bulunamadı")
        link='/error'
        return HttpResponseRedirect(link)

def menu(request,id):
    try:
        content=Content.objects.get(menu_id=id)
        link = '/content/' + str(content.id) + '/menu'
        return HttpResponseRedirect(link)
    except:
         messages.warning(request,"Hata! İlgili içerik bulunamadı")
         link='/error'
         return HttpResponseRedirect(link)


def error(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    menu = Menu.objects.all()
    context = {
        'category': category,
        'menu ': menu,
        'setting': setting,
    }
    return render(request, 'error_page.html', context)
