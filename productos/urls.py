from django.urls import path
from . import views

urlpatterns = [

    path('', views.lista_productos, name='lista_productos'),

    path(
        'entrada/',
        views.entrada_producto,
        name='entrada_producto'
    ),

    path(
    'movimientos/',
    views.historial_movimientos,
    name='historial_movimientos'
    ),
    path(
    'editar/<int:producto_id>/', 
    views.editar_producto, name='editar_producto'
    ),
    path(
    'eliminar/<int:producto_id>/', 
    views.eliminar_producto, name='eliminar_producto'
    ),
    path(
        'categorias/',
        views.lista_categorias,
        name='lista_categorias'
    ),
    path(
        'categorias/editar/<int:categoria_id>/', 
        views.editar_categoria, 
        name='editar_categoria'
    ),
    
    path(
        'categorias/eliminar/<int:categoria_id>/', 
        views.eliminar_categoria, 
        name='eliminar_categoria'
    ),
]