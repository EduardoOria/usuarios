from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Area(models.Model):
    nombre = models.CharField(max_length = 50, unique = True)
    cantidad_profesores = models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.nombre

    
class defaultUser(User):
    is_jefe = models.BooleanField()
    area = models.ForeignKey(Area, null=True, on_delete=models.CASCADE)
    cuenta = models.IntegerField()
   
    
    
class Producto(models.Model):
    nombre = models.CharField(max_length = 50, unique = True)
    precio = models.FloatField()
    cantidad = models.IntegerField()
    descripcion = models.TextField()
    def __str__(self) -> str:
        return self.nombre 


class Distribucion(models.Model):
    area = models.ForeignKey(Area, null=True, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, null=True, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    
    class Meta:
        # Especifica que la combinación de area y producto debe ser única
        unique_together = [['area', 'producto']]


class Asignacion(models.Model):
    user = models.ForeignKey(defaultUser, null=True, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, null=True, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    
    class Meta:
        # Especifica que la combinación de area y producto debe ser única
        unique_together = [['user', 'producto']]




class PagosAsignacion(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.FloatField()
    user = models.ForeignKey(defaultUser, null=True, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, null=True, on_delete=models.CASCADE)
    
    
class PagosDistribucion(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.FloatField()
    area = models.ForeignKey(Area, null=True, on_delete=models.CASCADE)
    
