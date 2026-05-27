from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto


class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    folio = models.CharField(max_length=20, blank=True, null=True)
    mesa = models.CharField(max_length=20, blank=True, null=True)
    numero_personas = models.PositiveIntegerField(default=1)
    dependiente = models.CharField(max_length=100, blank=True, null=True)
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    efectivo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transferencia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Venta #{self.id} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"

    @property
    def total_pagado(self):
        return self.efectivo + self.transferencia


class DetalleVenta(models.Model):
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT
    )
    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
    
class CierreJornada(models.Model):
    fecha = models.DateField(unique=True)
    total_vendido = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_efectivo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_transferencia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cantidad_ventas = models.PositiveIntegerField(default=0)

    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cierre {self.fecha}"