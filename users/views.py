from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from .models import Area, Asignacion, Distribucion, PagosAsignacion, PagosDistribucion, Producto, defaultUser as User
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import AreaCreateModelForm, AsignacionCreateModelForm, DistribucionCreateModelForm, ProductCreateModelForm, UsuarioModelForm,UsuarioUpdateModelForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
# Create your views here.



#
# Gestion de usuarios
#

class UserLoginView(LoginView):
    template_name = 'login.html'
    
    def get_success_url(self):
        
        user = self.request.user     
        if user.is_authenticated and not user.is_staff:
            if  not User.objects.get(id = user.id).is_jefe:     
              return reverse_lazy('listMisProductos')
            else:
              return reverse_lazy('listUser')
        return reverse_lazy('listUser')
    
class listUserView(LoginRequiredMixin ,UserPassesTestMixin,ListView):
    model = User
    template_name = 'user_list.html'  
    context_object_name = 'users'  
    
    def get_queryset(self):
        # Obtén el queryset base de todos los usuarios
        queryset = super().get_queryset()

        # Verifica si el usuario actual es un jefe
        try:
          user = User.objects.get(id = self.request.user.id)
          if user.is_jefe:
             queryset = queryset.filter(area=user.area)
        except:
            print('is_staff')
        return queryset
    
    def test_func(self):
        return self.request.user.is_staff or User.objects.get(id = self.request.user.id).is_jefe
    def handle_no_permission(self):
        return redirect('login')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
          context['is_jefe'] = User.objects.get(id = self.request.user.id).is_jefe
        except:
            context['is_jefe'] = False
        return context


class UserCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = User
    template_name = 'default_create.html'
    form_class = UsuarioModelForm
    success_url = reverse_lazy('listUser')
    def form_valid(self, form):
        # Get the instance being updated
        instance = form.instance
        area = instance.area
        
        area.cantidad_profesores += 1
        area.save()
        # Check if is_jefe is being set to True
        if instance.is_jefe:
            # Check if there's another user in the same area who is a boss
            existing_boss = User.objects.filter(area=instance.area, is_jefe=True).exclude(pk=instance.pk).exists()
            if existing_boss:
                # If there's an existing boss, return an error
                form.add_error('is_jefe', 'Ya existe un jefe en esta área.')
                return self.form_invalid(form)

        # Call the parent class's form_valid method
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.is_staff
    def handle_no_permission(self):
        return redirect('login')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Usuario'
        return context


class userUpdateview(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'default_edit.html'
    form_class = UsuarioUpdateModelForm
    success_url = reverse_lazy('listUser')
    
    def form_valid(self, form):
        # Get the instance being updated
        instance = form.instance

        # Check if is_jefe is being set to True
        if instance.is_jefe:
            # Check if there's another user in the same area who is a boss
            existing_boss = User.objects.filter(area=instance.area, is_jefe=True).exclude(pk=instance.pk).exists()
            if existing_boss:
                # If there's an existing boss, return an error
                form.add_error('is_jefe', 'Ya existe un jefe en esta área.')
                return self.form_invalid(form)

        # Call the parent class's form_valid method
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.is_staff 
    def handle_no_permission(self):
        return redirect('login')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Usuario'
        return context
    
class userDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'default_delete.html'
    success_url = reverse_lazy('listUser')
    
    
    def form_valid(self, form):
       
        user = self.get_object()
        
        area = user.area
        
        area.cantidad_profesores -= 1
        area.save()
      
        
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.is_staff
    def handle_no_permission(self):
        return redirect('login')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Usuario'
        return context
    
    
    
 #
 # Gestion de productos
 #   
 
class listProducView(LoginRequiredMixin,UserPassesTestMixin ,ListView):
    model = Producto
    template_name = 'producto_list.html'  
    context_object_name = 'productos'  
    
    def get_queryset(self):
        # Obtén el queryset base de todos los usuarios
        queryset = super().get_queryset()

        # Verifica si el usuario actual es un jefe
        try:
          user = User.objects.get(id = self.request.user.id)
          if user.is_jefe:
             queryset = Distribucion.objects.all().filter(area=user.area)
        except:
            print('is_staff')
        return queryset
    
    
    def test_func(self):
        return self.request.user.is_staff or User.objects.get(id = self.request.user.id).is_jefe
    def handle_no_permission(self):
        return redirect('login')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
          context['is_jefe'] = User.objects.get(id = self.request.user.id).is_jefe 
        except:
          context['is_jefe'] = False
        return context


class ProductCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Producto
    template_name = 'default_create.html'
    form_class = ProductCreateModelForm
    success_url = reverse_lazy('listProduct')
    
    def test_func(self):
        return self.request.user.is_staff 
    def handle_no_permission(self):
        return redirect('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Producto'
        return context
    
    


class ProductUpdateview(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Producto
    template_name = 'default_edit.html'
    form_class = ProductCreateModelForm
    success_url = reverse_lazy('listProduct')
    
    def test_func(self):
        return self.request.user.is_staff 
    def handle_no_permission(self):
        return redirect('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Producto'
        return context
    
class ProductDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Producto
    template_name = 'default_delete.html'
    success_url = reverse_lazy('listProduct')
    
    
    def test_func(self):
        return self.request.user.is_staff 
    def handle_no_permission(self):
        return redirect('login')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Producto'
        return context
    
    
#
# Gestion de Areas
#


class listAreaView(LoginRequiredMixin ,UserPassesTestMixin,ListView):
    model = Area
    template_name = 'area_list.html'  
    context_object_name = 'areas'  
    
    def test_func(self):
        return self.request.user.is_staff
    def handle_no_permission(self):
        return redirect('login')
    


class AreaCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Area
    template_name = 'default_create.html'
    form_class = AreaCreateModelForm
    success_url = reverse_lazy('listAreas')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Área'
        return context
    
    def test_func(self):
        return self.request.user.is_staff
    def handle_no_permission(self):
        return redirect('login')
    
    


class AreaUpdateview(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Area
    template_name = 'default_edit.html'
    form_class = AreaCreateModelForm
    success_url = reverse_lazy('listAreas')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Área'
        return context
    
    def test_func(self):
        return self.request.user.is_staff
    def handle_no_permission(self):
        return redirect('login')
    
class AreaDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Area
    template_name = 'default_delete.html'
    success_url = reverse_lazy('listAreas')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Área'
        return context
    
    def test_func(self):
        return self.request.user.is_staff
    def handle_no_permission(self):
        return redirect('login')
    
    
    
   
#
# Gestion de Distribucion
#


class listDistribucionView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Distribucion
    template_name = 'distribucion_list.html'  
    context_object_name = 'distribuciones' 
     
    def test_func(self):
        return self.request.user.is_staff
    def handle_no_permission(self):
        return redirect('login')
    

class DistribucionCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Distribucion
    template_name = 'default_create.html'
    form_class = DistribucionCreateModelForm
    success_url = reverse_lazy('listDistribuciones')
    
    
    def form_valid(self, form):
        instance = form.instance
        cantidad = instance.cantidad
        producto = instance.producto
        if cantidad > producto.cantidad:
                form.add_error('cantidad', 'La canidad no puede superar la existencia de producto')
                return self.form_invalid(form)
        if cantidad <=0:
                form.add_error('cantidad', 'Debes Distribuir almenos 1 producto')
                return self.form_invalid(form)
        
        t = super().form_valid(form)
        
        
        
        producto.cantidad = producto.cantidad - cantidad 
        producto.save()
        return t
    
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Distribución'
        return context
    
    def test_func(self):
        return self.request.user.is_staff
    def handle_no_permission(self):
        return redirect('login')
    


class DistribucionUpdateview(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Distribucion
    template_name = 'default_edit.html'
    form_class = DistribucionCreateModelForm
    success_url = reverse_lazy('listDistribuciones')
    
    def get_success_url(self) -> str:
        messages.success(self.request, 'asdasdadasdasdasdasdasd')
        return super().get_success_url()
    
    def form_valid(self, form):
        instance = form.instance
        cantidad = instance.cantidad
        producto = instance.producto
        cantidad = cantidad - Distribucion.objects.get(id = instance.id).cantidad
        
        if cantidad > producto.cantidad:
                form.add_error('cantidad', 'La canidad no puede superar la existencia de producto')
                return self.form_invalid(form)
        if cantidad <=0:
                form.add_error('cantidad', 'Debes Distribuir almenos 1 producto')
                return self.form_invalid(form)
        
        t = super().form_valid(form)
        print(cantidad)
        producto.cantidad = producto.cantidad - cantidad 
        producto.save()
        return t
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Distribución'
        return context
    
    def test_func(self):
        return self.request.user.is_staff
    def handle_no_permission(self):
        return redirect('login')
    
class DistribucionDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Distribucion
    template_name = 'default_delete.html'
    success_url = reverse_lazy('listDistribuciones')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Distribución'
        return context
    
    def test_func(self):
        return self.request.user.is_staff
    def handle_no_permission(self):
        return redirect('login')
    
    
    def form_valid(self, form):
       
        distribucion = self.get_object()
        
        producto = distribucion.producto
        producto.cantidad += distribucion.cantidad
        producto.save()
        
       
        
        return super().form_valid(form)
    
    
    
      
#
# Gestion de Asignacion
#


class listAsignacionView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Asignacion
    template_name = 'asignacion_list.html'  
    context_object_name = 'asignaciones' 
     
    def test_func(self):
        if self.request.user.is_staff:
           return False
        else:
            return User.objects.get(id = self.request.user.id).is_jefe 
    def handle_no_permission(self):
        return redirect('login')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
          context['is_jefe'] = User.objects.get(id = self.request.user.id).is_jefe
        except:
            context['is_jefe'] = False
        return context
    

class AsignacionCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Asignacion
    template_name = 'default_create.html'
    form_class = AsignacionCreateModelForm
    success_url = reverse_lazy('listAsignaciones')
    
    
    def form_valid(self, form):
        
        
        
        t = super().form_valid(form)
        user = User.objects.get(id = self.request.user.id)
        instance = form.instance
        cantidad = instance.cantidad
        producto = instance.producto
        distribucion = Distribucion.objects.get(area = user.area, producto = producto)
        distribucion.cantidad = distribucion.cantidad - cantidad 
        distribucion.save()
        return t
    
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Asignación'
        return context
    
    def test_func(self):
        if self.request.user.is_staff:
           return False
        else:
            return User.objects.get(id = self.request.user.id).is_jefe 
    def handle_no_permission(self):
        return redirect('login')
    


class AsignacionUpdateview(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Asignacion
    template_name = 'default_edit.html'
    form_class = AsignacionCreateModelForm
    success_url = reverse_lazy('listAsignaciones')
    
    
    
    def form_valid(self, form):
        
        #te falta cosigo
        user = User.objects.get(id = self.request.user.id)
        
        instance = form.instance
        cantidad = instance.cantidad
        producto = instance.producto
        cantidad = cantidad - Asignacion.objects.get(id = instance.id).cantidad
        t = super().form_valid(form)
        
        
        distribucion = Distribucion.objects.get(area = user.area, producto = producto)
        distribucion.cantidad = distribucion.cantidad - cantidad 
        distribucion.save()
        return t
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Asignación'
        return context
    
    def test_func(self):
        if self.request.user.is_staff:
           return False
        else:
            return User.objects.get(id = self.request.user.id).is_jefe 
    def handle_no_permission(self):
        return redirect('login')
    
class AsignacionDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Asignacion
    template_name = 'default_delete.html'
    success_url = reverse_lazy('listAsignaciones')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Asignacion'
        return context
    
    def test_func(self):
        if self.request.user.is_staff:
           return False
        else:
            return User.objects.get(id = self.request.user.id).is_jefe 
    def handle_no_permission(self):
        return redirect('login')
    
    def form_valid(self, form):
        # Obtener el objeto Asignacion que se eliminará
        asignacion = self.get_object()
        user = User.objects.get(id=self.request.user.id)
        distribucion = Distribucion.objects.get(area=user.area, producto=asignacion.producto)
        distribucion.cantidad += asignacion.cantidad
        distribucion.save()
        
        # Mensaje de éxito
      
        
        return super().form_valid(form)
    
    
    
    
    
    #
    # Mis Productos
    #
    
    
    
    
    
class listMisProductosView(LoginRequiredMixin,UserPassesTestMixin ,ListView):
    model = Producto
    template_name = 'misproductos_list.html'  
    context_object_name = 'productos'  
    
    def get_queryset(self):
        # Obtén el queryset base de todos los usuarios
        queryset = super().get_queryset()

        # Verifica si el usuario actual es un jefe
        try:
          user = User.objects.get(id = self.request.user.id)
          queryset = Asignacion.objects.all().filter(user = user)
        except:
            print('is_staff')
        return queryset
    
    
    def test_func(self):
        return  self.request.user.is_staff == False
    def handle_no_permission(self):
        return redirect('login')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
          context['is_jefe'] = User.objects.get(id = self.request.user.id).is_jefe 
        except:
          context['is_jefe'] = False
        return context
    
    
def comprar(request,pk):
    try:    
        asignacion = Asignacion.objects.get(id = pk)
        user = User.objects.get(id = request.user.id)
        
        if asignacion.user == user:
            PagosAsignacion.objects.create(monto = asignacion.cantidad*asignacion.producto.precio,user = User.objects.get(id = request.user.id), area = User.objects.get(id = request.user.id).area)
            asignacion.delete()
    except:
        print('na')
    return redirect('listMisProductos')
   
   
def desechar(request,pk):
    try:
        asignacion = Asignacion.objects.get(id = pk)
        user = User.objects.get(id = request.user.id)
        
        if asignacion.user == user:
            distribucion = Distribucion.objects.get(area = user.area, producto = asignacion.producto)
            distribucion.cantidad += asignacion.cantidad
            distribucion.save()
            asignacion.delete()
    except:
     
    return redirect('listMisProductos')
     
     
def comprarAsignacion(request):
    try:
        user = User.objects.get(id = request.user.id)
        if user.is_jefe:
            area = user.area
            pagoT = 0
            try:
            
             for dis  in  Distribucion.objects.all().filter(area = area):
                 
                 pago = dis.cantidad * dis.producto.precio
                 pagoT += pago
            except:
                pagoT = Distribucion.objects.get(area = area).producto.precio
            PagosDistribucion.objects.create(monto = pagoT, area = User.objects.get(id = request.user.id).area)
        
    except Exception as e:
        print(e)
    return redirect('listProduct')
    


class listPagosA(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = PagosAsignacion
    template_name = 'pagos_default_list.html'  
    context_object_name = 'pagos' 
    
    def get_queryset(self):
        # Obtén el queryset base de todos los usuarios
        queryset = super().get_queryset()

        # Verifica si el usuario actual es un jefe
        try:
          user = User.objects.get(id = self.request.user.id)
          queryset =  queryset.filter(area = user.area)
        except:
            print('is_staff')
        return queryset
     
     
    def test_func(self):
        if self.request.user.is_staff:
           return False
        else:
            return User.objects.get(id = self.request.user.id).is_jefe 
    def handle_no_permission(self):
        return redirect('login')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
          context['is_jefe'] = User.objects.get(id = self.request.user.id).is_jefe
        except:
            context['is_jefe'] = False
        return context
    
    


class listPagosD(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = PagosDistribucion   
    template_name = 'pagos_default_list.html'  
    context_object_name = 'pagos' 
     
    def test_func(self):
        return self.request.user.is_staff
       
    def handle_no_permission(self):
        return redirect('login')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
          context['is_jefe'] = User.objects.get(id = self.request.user.id).is_jefe
        except:
            context['is_jefe'] = False
        return context