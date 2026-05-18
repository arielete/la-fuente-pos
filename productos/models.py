from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    TIPO_PRODUCTO = [
        ('venta', 'Producto de venta'),
        ('enlatado', 'Enlatado / directo'),
        ('ingrediente', 'Ingrediente'),
    ]

    UNIDADES_MEDIDA = [
        ('unidad', 'Unidad'),
        ('kg', 'Kilogramo'),
        ('g', 'Gramo'),
        ('lb', 'Libra'),
        ('litro', 'Litro'),
        ('ml', 'Mililitro'),
        ('paquete', 'Paquete'),
    ]

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='productos'
    )
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_PRODUCTO,
        default='venta'
    )

    unidad_medida = models.CharField(
        max_length=20,
        choices=UNIDADES_MEDIDA,
        default='unidad'
    )

    precio = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
class EntradaProducto(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='entradas'
    )
    cantidad = models.DecimalField(
    max_digits=10,
    decimal_places=2
)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    motivo = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Entrada de {self.cantidad} - {self.producto.nombre}"


class MovimientoInventario(models.Model):
    TIPO_MOVIMIENTO = [
        ('entrada', 'Entrada'),
        ('venta', 'Venta'),
        ('ajuste', 'Ajuste'),
    ]

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='movimientos'
    )
    tipo = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO)
    cantidad = models.DecimalField(
    max_digits=10,
    decimal_places=2)

    stock_anterior = models.DecimalField(
    max_digits=10,
    decimal_places=2)

    stock_nuevo = models.DecimalField(
    max_digits=10,
    decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} - {self.cantidad}"