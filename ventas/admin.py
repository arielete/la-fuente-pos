from django.contrib import admin
from .models import Venta, DetalleVenta, CierreJornada


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'folio',
        'mesa',
        'numero_personas',
        'dependiente',
        'fecha',
        'total',
        'efectivo',
        'transferencia',
        'usuario',
    )

    search_fields = (
        'folio',
        'mesa',
        'dependiente',
    )

    list_filter = (
        'fecha',
        'usuario',
    )


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'venta',
        'producto',
        'cantidad',
        'precio_unitario',
        'subtotal',
    )

    search_fields = (
        'producto__nombre',
    )

    list_filter = (
        'producto',
    )


@admin.register(CierreJornada)
class CierreJornadaAdmin(admin.ModelAdmin):
    list_display = (
        'fecha',
        'total_vendido',
        'total_efectivo',
        'total_transferencia',
        'cantidad_ventas',
        'usuario',
    )

    list_filter = (
        'fecha',
        'usuario',
    )