from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput, Select, FileInput
from django.urls import reverse
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from home.models import UserProfile


class Category(MPTTModel):
    STATUS =(
        ('True','Evet'),
        ('False','Hayır'),
    )
    title = models.CharField(max_length=100)
    description = models.CharField(blank=True, max_length=225)
    keywords = models.CharField(blank=True, max_length=225)
    image=models.ImageField(blank=True,upload_to='image/')
    status=models.CharField(max_length=10, choices=STATUS)
    slug=models.SlugField(null=False,unique=True)
    parent= TreeForeignKey('self',blank=True,null=True, related_name='children', on_delete=models.CASCADE)
    create_at= models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)

    class MPTTMeta:

        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k=self.parent
        while k is not None:
            full_path.append(k.title)
            k=k.parent
        return ' / '.join(full_path[::-1])


    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug':self.slug})

class Product(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )


    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category= models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(blank=True, max_length=150)
    isim = models.CharField(blank=True, max_length=150)
    email = models.CharField(blank=True, max_length=150)
    telefon = models.CharField(blank=True, max_length=150)
    description = models.CharField(blank=True, max_length=225)
    keywords = models.CharField(blank=True, max_length=225)
    image = models.ImageField(blank=True, upload_to='image/')
    price=models.FloatField()
    marka = models.CharField(blank=True, max_length=150)
    model = models.CharField(blank=True, max_length=225)
    modelyili = models.IntegerField()
    km = models.IntegerField()
    amount = models.IntegerField()
    yakit = models.CharField(blank=True, max_length=225)
    vites = models.CharField(blank=True, max_length=225)
    govde = models.CharField(blank=True, max_length=150)
    disrenk = models.CharField(blank=True, max_length=225)
    icrenk = models.CharField(blank=True, max_length=225)
    doseme = models.CharField(blank=True, max_length=225)
    kaplama = models.CharField(blank=True, max_length=225)
    motorhacmi = models.IntegerField()
    motorgucu = models.IntegerField()
    detail=RichTextUploadingField()
    slug = models.SlugField(null=False,unique=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title


    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def catimg_tag(self):
        return mark_safe((Category.status))

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})



class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category' ,'title', 'slug', 'keywords', 'description', 'image', 'detail','price','marka','disrenk','model','modelyili','km','amount','yakit','vites','govde',
                  'icrenk','doseme','kaplama','motorhacmi','motorgucu', 'isim','email','telefon']
        widgets = {
            'title'     : TextInput(attrs={'class': 'input', 'placeholder': ''}),
            'slug'  : TextInput(attrs={'class': 'input', 'placeholder': ''}),
            'keywords'    : TextInput(attrs={'class': 'input', 'placeholder': ''}),
            'description'  : TextInput(attrs={'class': 'input', 'placeholder': ''}),
            'category': Select(attrs={'class': 'input', 'placeholder': ''},choices=Category.objects.all()),
            'image': FileInput(attrs={'class': 'input', 'placeholder': ''}),
            'detail': CKEditorWidget(),
            'price':TextInput(attrs={'class': 'input', 'placeholder': ''}),
            'marka':TextInput(attrs={'class': 'input', 'placeholder': ''}),
            'model':TextInput(attrs={'class': 'input', 'placeholder': ''}),
            'modelyili':TextInput(attrs={'class': 'input', 'placeholder': ''}),
            'km':TextInput(attrs={'class': 'input', 'placeholder': ''}),
            'amount':TextInput(attrs={'class': 'input', 'placeholder': ''}),
            'yakit':TextInput(attrs={'class': 'input', 'placeholder': ''}),
            'vites':TextInput(attrs={'class': 'input', 'placeholder': ''}),
            'govde':TextInput(attrs={'class': 'input', 'placeholder': ''}),
            'icrenk':TextInput(attrs={'class': 'input', 'placeholder': ''}),
            'disrenk':TextInput(attrs={'class': 'input', 'placeholder': ''}),
            'doseme':TextInput(attrs={'class': 'input', 'placeholder': ''}),
            'kaplama':TextInput(attrs={'class': 'input', 'placeholder': ''}),
            'motorhacmi':TextInput(attrs={'class': 'input', 'placeholder': ''}),
            'motorgucu':TextInput(attrs={'class': 'input', 'placeholder': ''}),
            'isim' : TextInput(attrs={'class': 'input', 'placeholder': ''}),
            'email' : TextInput(attrs={'class': 'input', 'placeholder': ''}),
            'telefon' :TextInput(attrs={'class': 'input', 'placeholder': ''}),
        }


class Images(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(blank=True, upload_to='image/')
    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

class ImagesForm(ModelForm):
    class Meta:
        model = Images
        fields = ['title', 'image']

class Comment(models.Model):
    STATUS = (
        ('New','Yeni'),
        ('True','Evet'),
        ('False','Hayır'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   # userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    comment = models.TextField(max_length=200)
    status = models.CharField(max_length=10,choices=STATUS, default='New')
    ip= models.CharField(max_length=50, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment']
