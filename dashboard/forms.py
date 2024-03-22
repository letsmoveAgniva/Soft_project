from django import forms
from .models import Product, Order, Information

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','category','quantity', 'buying_price', 'selling_price']
        
class OrderForm(forms.ModelForm):
     
    class Meta:
        model=Order
        fields = ['product','order_quantity']       
        
        
        
class InformationForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = ['content']        
        
class OrderUpdateForm(forms.ModelForm):
     
    class Meta:
        model=Order
        fields = ['status']
        
class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','category','quantity', 'selling_price']