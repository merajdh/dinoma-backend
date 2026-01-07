from django.contrib import admin
from store.models import Product ,Audience , ClothingType ,Gallery,Specification ,Size ,Color  , Cart , CartOrder , CartOrderItem , Review
from django import forms
from django.utils.formats import number_format
# Register your models here.

class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 0


class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 0

class SizeInline(admin.TabularInline):
    model = Size
    extra = 0



class ColorInlineForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = '__all__'
        widgets = {
            'color_code': forms.TextInput(attrs={'type': 'color'}),
            'color_text': forms.TextInput(attrs={'type': 'color'})
        }


class ColorInline(admin.TabularInline):
    model = Color
    extra = 0
    form = ColorInlineForm  

class ProductAdmin(admin.ModelAdmin):
    list_display = ("title" , 'price_fa' ,'audience' , 'clothing_type', 'shipping_price_fa' , 'stock_qty' , 'in_stock' , 'featured')
    list_editable = ["featured"]
    list_filter =  ['date']
    search_fields = ['title']
    inlines = [GalleryInline , SpecificationInline,SizeInline ,ColorInline ]
    def price_fa(self, obj):
        return f"{number_format(obj.price, use_l10n=True, force_grouping=True)} ریال"
    def shipping_price_fa(self, obj):
        return f"{number_format(obj.shipping_amount, use_l10n=True, force_grouping=True)} ریال"
    price_fa.short_description = "قیمت"
    shipping_price_fa.short_description = "قیمت ارسال"


class ReviewAdmin(admin.ModelAdmin):
    list_display = ["product" , 'user']


    
admin.site.register(Product , ProductAdmin )
admin.site.register( Audience  )
admin.site.register( ClothingType  )
admin.site.register( Cart  )
admin.site.register( CartOrder  )
admin.site.register( CartOrderItem  )
admin.site.register( Review , ReviewAdmin )
