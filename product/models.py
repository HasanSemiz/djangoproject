from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


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
    slug=models.SlugField()
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
class Product(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    category= models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(blank=True, max_length=150)
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
    slug = models.SlugField(blank=True, max_length=150)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title


    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class Images(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(blank=True, upload_to='image/')
    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

class Comment(models.Model):
    STATUS = (
        ('New','Yeni'),
        ('True','Evet'),
        ('False','Hayır'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
        fields =['subject','comment']

