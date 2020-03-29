from django.contrib import admin
from product.models import Category, Product, Images

class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 5


class CatagoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status','image_tag']
    list_filter = ['status']
    readonly_fields = ('image_tag',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category','price','amount', 'status']
    list_filter = ['status','category']
    inlines = [ProductImageInline]

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'image_tag']
    readonly_fields = ('image_tag',)

admin.site.register(Category,CatagoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images, ImagesAdmin)