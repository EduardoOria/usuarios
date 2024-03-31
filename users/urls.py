from django.contrib import admin
from django.urls import path
from django.urls import include
from .views import AreaCreateView, AreaDeleteView, AreaUpdateview, AsignacionCreateView, AsignacionDeleteView, AsignacionUpdateview, DistribucionCreateView, DistribucionDeleteView, DistribucionUpdateview, ProductDeleteView, ProductUpdateview, UserLoginView, comprar, comprarAsignacion, desechar, listAreaView, listAsignacionView, listDistribucionView, listMisProductosView, listPagosA, listPagosD, listProducView,ProductCreateView, listUserView, UserCreateView, userUpdateview, userDeleteView
from django.contrib.auth.views import LogoutView

urlpatterns = [
     path('logout/',LogoutView.as_view(next_page='/'), name='logout'),
    path('',UserLoginView.as_view(), name='login'),
    path('users/',listUserView.as_view(), name = 'listUser'),
    path('createuser/', UserCreateView.as_view(), name = 'crearuser'),
    path('editaruser/<int:pk>',userUpdateview.as_view() ,name = 'editaruser'),
    path('eliminaruser/<int:pk>',userDeleteView.as_view() ,name = 'eliminaruser'),
    
    
    path('products/', listProducView.as_view(), name='listProduct'),
    path('createproduct/', ProductCreateView.as_view(), name = 'crearproduct'),
    path('editarproduct/<int:pk>',ProductUpdateview.as_view() ,name = 'editarproduct'),
    path('eliminarproduct/<int:pk>',ProductDeleteView.as_view() ,name = 'eliminarproduct'),
    
    
    
    path('areas/', listAreaView.as_view(), name='listAreas'),
    path('createarea/', AreaCreateView.as_view(), name = 'creararea'),
    path('editararea/<int:pk>',AreaUpdateview.as_view() ,name = 'editararea'),
    path('eliminararea/<int:pk>',AreaDeleteView.as_view() ,name = 'eliminararea'),
    
    
    
    
    path('distribuciones/', listDistribucionView.as_view(), name='listDistribuciones'),
    path('createdistribucion/', DistribucionCreateView.as_view(), name = 'creardistribucion'),
    path('editardistribucion/<int:pk>',DistribucionUpdateview.as_view() ,name = 'editardistribucion'),
    path('eliminardistribucion/<int:pk>',DistribucionDeleteView.as_view() ,name = 'eliminardistribucion'),
    
    
    path('asignaciones/', listAsignacionView.as_view(), name='listAsignaciones'),
    path('createasignacion/', AsignacionCreateView.as_view(), name = 'crearasignacion'),
    path('editarasignacion/<int:pk>',AsignacionUpdateview.as_view() ,name = 'editarasignacion'),
    path('eliminarasignacion/<int:pk>',AsignacionDeleteView.as_view() ,name = 'eliminarasignacion'),
    
    path('misproductos/', listMisProductosView.as_view(), name='listMisProductos'),
    
    path('comprarproduct/<int:pk>',comprar ,name = 'comprarproduct'),
    path('denegarproduct/<int:pk>',desechar ,name = 'denegarproduct'),
    
    
    path('comprardistribucion/',comprarAsignacion ,name = 'comprard'),

    
    
    path('pagosA/', listPagosA.as_view(), name='pagosa'),
    
    path('pagosD/', listPagosD.as_view(), name='pagosd'),
    
]