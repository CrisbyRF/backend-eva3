from django.db import models

# Create your models here.
class ProductoModel(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    stock = models.IntegerField()
    precio_unitario = models.IntegerField()
    fecha_ingreso = models.DateField()
    categoria = models.CharField(max_length=30)