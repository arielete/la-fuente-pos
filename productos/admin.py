from django.contrib import admin
from .models import Categoria, Producto, EntradaProducto, MovimientoInventario


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'activa')
    search_fields = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
        'categoria',
        'tipo',
        'unidad_medida',
        'precio',
        'stock',
        'activo'
    )

    list_filter = (
        'categoria',
        'tipo',
        'unidad_medida',
        'activo'
    )

    search_fields = (
        'nombre',
        'categoria__nombre',
    )


@admin.register(EntradaProducto)
class EntradaProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'cantidad', 'fecha', 'usuario', 'motivo')
    list_filter = ('fecha', 'producto')
    search_fields = ('producto__nombre', 'motivo')


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'producto',
        'tipo',
        'cantidad',
        'stock_anterior',
        'stock_nuevo',
        'fecha',
        'usuario'
    )
    list_filter = ('tipo', 'fecha', 'producto')
    search_fields = ('producto__nombre', 'descripcion')