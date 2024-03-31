# from django.test import TestCase

# # Create your tests here.
# from django.test import TestCase
# from .models import Area, defaultUser, Producto, Distribucion, Asignacion

# class PruebasModelos(TestCase):

#     def setUp(self):
#         self.area = Area.objects.create(nombre='Área de Prueba', cantidad_profesores=3)
#         self.user = defaultUser.objects.create_user(username='usuario_prueba', password='contrasena', is_jefe=False, area=self.area, cuenta=12345)
#         self.producto = Producto.objects.create(nombre='Producto de Prueba', precio=10.0, cantidad=100, descripcion='Descripción de prueba')
#         self.distribucion = Distribucion.objects.create(area=self.area, producto=self.producto, cantidad=50)
#         self.asignacion = Asignacion.objects.create(user=self.user, producto=self.producto, cantidad=10)

#     def test_insertar_area(self):
#         nueva_area = Area.objects.create(nombre='Nueva Área', cantidad_profesores=5)
#         self.assertEqual(nueva_area.nombre, 'Nueva Área')

#     def test_modificar_producto(self):
#         producto = Producto.objects.get(nombre='Producto de Prueba')
#         producto.precio = 15.0
#         producto.save()
#         self.assertEqual(producto.precio, 15.0)

#     def test_listar_distribuciones(self):
#         distribuciones = Distribucion.objects.all()
#         self.assertGreaterEqual(distribuciones.count(), 1)

#     def test_eliminar_asignacion(self):
#         asignacion = Asignacion.objects.get(user=self.user)
#         asignacion.delete()
#         with self.assertRaises(Asignacion.DoesNotExist):
#             Asignacion.objects.get(user=self.user)

from django.test import TestCase
from .models import Area, defaultUser, Producto, Distribucion, Asignacion
from django.db.utils import IntegrityError

class PruebasModelos(TestCase):

    def test_valores_negativos(self):
        with self.assertRaises(IntegrityError):
            producto = Producto.objects.create(nombre='Producto Negativo', precio=-10.0, cantidad=-100, descripcion='Descripción negativa')

    def test_insertar_duplicados(self):
        area = Area.objects.create(nombre='Área Duplicada', cantidad_profesores=3)
        with self.assertRaises(IntegrityError):
            Area.objects.create(nombre='Área Duplicada', cantidad_profesores=5)

        producto = Producto.objects.create(nombre='Producto Duplicado', precio=10.0, cantidad=100, descripcion='Descripción duplicada')
        with self.assertRaises(IntegrityError):
            Producto.objects.create(nombre='Producto Duplicado', precio=15.0, cantidad=200, descripcion='Otra descripción')

        user = defaultUser.objects.create_user(username='usuario_duplicado', password='contrasena', is_jefe=False, area=area, cuenta=12345)
        with self.assertRaises(IntegrityError):
            defaultUser.objects.create_user(username='usuario_duplicado', password='otracontrasena', is_jefe=True, area=area, cuenta=54321)