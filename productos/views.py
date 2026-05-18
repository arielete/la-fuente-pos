from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import (Producto,
                        MovimientoInventario,
                        Categoria)
from .forms import EntradaProductoForm, ProductoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def lista_productos(request):
    productos = Producto.objects.all().order_by('nombre')

    formularios = {
        producto.id: ProductoForm(instance=producto)
        for producto in productos
    }
    
    categorias = Categoria.objects.all().order_by('nombre')

    return render(request, 'productos/lista_productos.html', {
        'productos': productos,
        'formularios': formularios,
        'categorias': categorias,
    })
    



@login_required
def entrada_producto(request):

    productos = Producto.objects.filter(
        activo=True,
        tipo__in=['enlatado', 'ingrediente']
    ).select_related('categoria').order_by(
        'tipo',
        'categoria__nombre',
        'nombre'
    )

    productos_por_categoria = {}

    for producto in productos:
        categoria = producto.categoria.nombre if producto.categoria else 'Sin categoría'

        if categoria not in productos_por_categoria:
            productos_por_categoria[categoria] = []

        productos_por_categoria[categoria].append(producto)

    if request.method == 'POST':

        form = EntradaProductoForm(request.POST)

        if form.is_valid():

            entrada = form.save(commit=False)

            producto = entrada.producto
            stock_anterior = producto.stock

            producto.stock += entrada.cantidad
            stock_nuevo = producto.stock
            producto.save()

            entrada.usuario = request.user
            entrada.save()

            MovimientoInventario.objects.create(
                producto=producto,
                tipo='entrada',
                cantidad=entrada.cantidad,
                stock_anterior=stock_anterior,
                stock_nuevo=stock_nuevo,
                usuario=request.user,
                descripcion=entrada.motivo
            )

            return redirect('lista_productos')

    else:
        form = EntradaProductoForm()

    return render(request, 'productos/entrada_producto.html', {
        'form': form,
        'productos_por_categoria': productos_por_categoria
    })
    
    
@login_required
def historial_movimientos(request):
    movimientos = MovimientoInventario.objects.exclude(
        tipo='venta'
    ).order_by('-fecha')

    return render(request, 'productos/historial_movimientos.html', {
        'movimientos': movimientos
    })
    
@login_required
def editar_producto(request, producto_id):

    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':

        producto.nombre = request.POST.get('nombre')
        producto.categoria_id = request.POST.get('categoria')
        producto.descripcion = request.POST.get('descripcion')
        producto.precio = request.POST.get('precio')
        producto.stock = request.POST.get('stock')

        producto.activo = 'activo' in request.POST

        producto.save()

        messages.success(
            request,
            'Producto actualizado correctamente.'
        )

    return redirect('lista_productos')


@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')

    return redirect('lista_productos')


@login_required
def lista_categorias(request):

    categorias = Categoria.objects.all().order_by('nombre')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')

        if nombre:
            Categoria.objects.create(nombre=nombre)

            messages.success(request, 'Categoría creada correctamente')

            return redirect('lista_categorias')

    return render(
        request,
        'productos/categorias.html',
        {
            'categorias': categorias
        }
    )

@login_required
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        activa = 'activa' in request.POST

        if nombre:
            categoria.nombre = nombre
            categoria.activa = activa
            categoria.save()

            messages.success(request, 'Categoría actualizada correctamente.')

    return redirect('lista_categorias')


@login_required
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)

    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada correctamente.')

    return redirect('lista_categorias')