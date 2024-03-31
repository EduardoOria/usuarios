from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Area, Asignacion, Distribucion, Producto, defaultUser as User

class UsuarioModelForm(UserCreationForm):

  class Meta:
    model = User
    fields = ('username','first_name','last_name', 'password1', 'password2','is_jefe','area', 'cuenta')
    
    
    

class UsuarioUpdateModelForm(forms.ModelForm):

  class Meta:
    model = User
    fields = ('username','first_name','last_name','is_jefe','area', 'cuenta')
    
class ProductCreateModelForm(forms.ModelForm):
  class Meta:
    model = Producto
    fields = '__all__'
  
class AreaCreateModelForm(forms.ModelForm):
  class Meta:
    model = Area
    fields = ('nombre',)
      
class DistribucionCreateModelForm(forms.ModelForm):
  
  class Meta:
    model = Distribucion
    fields = '__all__'
    

class AsignacionCreateModelForm(forms.ModelForm):
  
  class Meta:
    model = Asignacion
    fields = '__all__'