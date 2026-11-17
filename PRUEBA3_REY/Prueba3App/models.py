from django.contrib.auth.models import User
from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.TextField(verbose_name='Descripción')
    stock = models.PositiveIntegerField(verbose_name='Stock')
    precio_unitario = models.PositiveIntegerField(verbose_name='Precio unitario')
    fecha_ingreso = models.DateField(verbose_name='Fecha de ingreso')
    categoria = models.CharField(max_length=100, verbose_name='Categoría')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']

    def __str__(self):
        return f'{self.nombre} ({self.categoria})'


class RegistroAcceso(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuario autenticado',
    )
    usuario_ingresado = models.CharField(
        max_length=150,
        verbose_name='Nombre de usuario ingresado',
    )
    exitoso = models.BooleanField(
        default=False,
        verbose_name='Acceso exitoso',
    )
    detalle = models.CharField(
        max_length=150,
        verbose_name='Detalle del evento',
    )
    fecha_hora = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha y hora',
    )

    class Meta:
        verbose_name = 'Registro de acceso'
        verbose_name_plural = 'Registros de acceso'
        ordering = ['-fecha_hora']

    def __str__(self):
        estado = 'EXITOSO' if self.exitoso else 'FALLIDO'
        return f'[{estado}] {self.usuario_ingresado} ({self.fecha_hora:%d-%m-%Y %H:%M})'
