from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import(
    AgregarProductoForm,
    ConfirmarVentaForm
)
from .models import Venta, DetalleVenta, CierreJornada
from productos.models import MovimientoInventario
from productos.models import Producto
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from collections import defaultdict

@login_required
def nueva_venta(request):

    if 'carrito' not in request.session:
        request.session['carrito'] = []

    carrito = request.session['carrito']

    if request.method == 'POST':

        accion = request.POST.get('accion')

        if accion == 'eliminar':
            indice = int(request.POST.get('indice'))

            if 0 <= indice < len(carrito):
                carrito.pop(indice)

            request.session['carrito'] = carrito
            request.session.modified = True

            return redirect('nueva_venta')

        if accion == 'agregar':
            producto_form = AgregarProductoForm(request.POST)

            if producto_form.is_valid():
                producto = producto_form.cleaned_data['producto']
                cantidad = producto_form.cleaned_data['cantidad']

                subtotal = producto.precio * cantidad

                carrito.append({
                    'producto_id': producto.id,
                    'nombre': producto.nombre,
                    'cantidad': float(cantidad),
                    'precio': float(producto.precio),
                    'subtotal': float(subtotal),
                })

                request.session['carrito'] = carrito
                request.session.modified = True

                return redirect('nueva_venta')

        if accion == 'confirmar':
            venta_form = ConfirmarVentaForm(request.POST)

            if not carrito:
                messages.error(request, 'No puedes registrar una venta sin productos.')
                return redirect('nueva_venta')

            if venta_form.is_valid():

                folio = venta_form.cleaned_data['folio']
                mesa = venta_form.cleaned_data['mesa']
                numero_personas = venta_form.cleaned_data['numero_personas']
                dependiente = venta_form.cleaned_data['dependiente']
                efectivo = venta_form.cleaned_data['efectivo']
                transferencia = venta_form.cleaned_data['transferencia']

                total = Decimal(str(sum(item['subtotal'] for item in carrito)))
                total_pagado = efectivo + transferencia

                hoy = timezone.now().date()

                if folio:
                    folio_existente = Venta.objects.filter(
                        folio=folio,
                        fecha__date=hoy
                    ).exists()

                    if folio_existente:
                        messages.error(
                            request,
                            f'Ya existe una comanda con el folio {folio} en el día de hoy.'
                        )
                        return redirect('nueva_venta')

                if total_pagado < total:
                    messages.error(request, f'Pago insuficiente. Total: ${total}')
                    return redirect('nueva_venta')

                if total_pagado > total:
                    messages.error(
                        request,
                        f'El pago no puede ser mayor que el total. Total exacto: ${total}'
                    )
                    return redirect('nueva_venta')

                # Validar stock antes de guardar la venta
                for item in carrito:
                    producto = Producto.objects.get(id=item['producto_id'])
                    cantidad = Decimal(str(item['cantidad']))

                    if producto.tipo != 'venta':
                        if producto.stock is not None and producto.stock < cantidad:
                            messages.error(
                                request,
                                f'No hay stock suficiente para {producto.nombre}'
                            )
                            return redirect('nueva_venta')

                # Crear venta
                venta = Venta.objects.create(
                    usuario=request.user,
                    folio=folio,
                    mesa=mesa,
                    numero_personas=numero_personas,
                    dependiente=dependiente,
                    total=total,
                    efectivo=efectivo,
                    transferencia=transferencia
                )

                # Crear detalles y descontar stock
                for item in carrito:
                    producto = Producto.objects.get(id=item['producto_id'])
                    cantidad = Decimal(str(item['cantidad']))
                    subtotal = Decimal(str(item['subtotal']))

                    DetalleVenta.objects.create(
                        venta=venta,
                        producto=producto,
                        cantidad=cantidad,
                        precio_unitario=producto.precio,
                        subtotal=subtotal
                    )

                    if producto.tipo != 'venta':
                        stock_anterior = producto.stock

                        producto.stock -= cantidad
                        stock_nuevo = producto.stock
                        producto.save()

                        MovimientoInventario.objects.create(
                            producto=producto,
                            tipo='venta',
                            cantidad=cantidad,
                            stock_anterior=stock_anterior,
                            stock_nuevo=stock_nuevo,
                            usuario=request.user,
                            descripcion=f'Venta #{venta.id}'
                        )

                request.session['carrito'] = []
                request.session.modified = True

                messages.success(request, 'Venta registrada correctamente.')
                return redirect('nueva_venta')

            messages.error(request, 'Revisa los datos de la comanda y el pago.')
            return redirect('nueva_venta')

    hoy = timezone.localdate()

    ultima_venta = Venta.objects.filter(
        fecha__date=hoy
    ).order_by('-id').first()

    if ultima_venta and ultima_venta.folio:
        proximo_folio = str(int(ultima_venta.folio) + 1)
    else:
        proximo_folio = '1'

    producto_form = AgregarProductoForm()
    venta_form = ConfirmarVentaForm(
        initial={'folio': proximo_folio}
    )

    total_general = sum(item['subtotal'] for item in carrito)

    productos = Producto.objects.filter(
        activo=True
    ).select_related('categoria').order_by(
        'categoria__nombre',
        'nombre'
    )

    productos_por_categoria = defaultdict(list)

    for producto in productos:
        categoria = producto.categoria.nombre if producto.categoria else 'Sin categoría'
        productos_por_categoria[categoria].append(producto)

    return render(request, 'ventas/nueva_venta.html', {
        'producto_form': producto_form,
        'venta_form': venta_form,
        'carrito': carrito,
        'total_general': total_general,
        'productos_por_categoria': dict(productos_por_categoria)
    })
    

@login_required
def historial_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha')

    return render(request, 'ventas/historial_ventas.html', {
        'ventas': ventas
    })
    
    
@login_required
def cierre_jornada(request):
    hoy = timezone.localdate()

    productos_vendidos = DetalleVenta.objects.filter(
        venta__fecha__date=hoy
    ).values(
        'producto__nombre'
    ).annotate(
        cantidad_vendida=Sum('cantidad'),
        total_vendido=Sum('subtotal')
    ).order_by(
        '-cantidad_vendida'
    ) 

    ventas_hoy = Venta.objects.filter(fecha__date=hoy)

    total_vendido = ventas_hoy.aggregate(Sum('total'))['total__sum'] or 0
    total_efectivo = ventas_hoy.aggregate(Sum('efectivo'))['efectivo__sum'] or 0
    total_transferencia = ventas_hoy.aggregate(Sum('transferencia'))['transferencia__sum'] or 0
    cantidad_ventas = ventas_hoy.count()

    cierre_existente = CierreJornada.objects.filter(fecha=hoy).first()

    if request.method == 'POST':
        if cierre_existente:
            messages.warning(request, 'El cierre de hoy ya fue guardado anteriormente.')
        else:
            CierreJornada.objects.create(
                fecha=hoy,
                total_vendido=total_vendido,
                total_efectivo=total_efectivo,
                total_transferencia=total_transferencia,
                cantidad_ventas=cantidad_ventas,
                usuario=request.user
            )

            messages.success(request, 'Cierre de jornada guardado correctamente.')

        return redirect('cierre_jornada')

    return render(request, 'ventas/cierre_jornada.html', {
        'hoy': hoy,
        'ventas_hoy': ventas_hoy,
        'total_vendido': total_vendido,
        'total_efectivo': total_efectivo,
        'total_transferencia': total_transferencia,
        'cantidad_ventas': cantidad_ventas,
        'cierre_existente': cierre_existente,
        'productos_vendidos': productos_vendidos,
    })
    
@login_required
def exportar_cierre_pdf(request):

    hoy = timezone.now().date()

    ventas_hoy = Venta.objects.filter(fecha__date=hoy)

    total_vendido = ventas_hoy.aggregate(Sum('total'))['total__sum'] or 0
    total_efectivo = ventas_hoy.aggregate(Sum('efectivo'))['efectivo__sum'] or 0
    total_transferencia = ventas_hoy.aggregate(Sum('transferencia'))['transferencia__sum'] or 0
    cantidad_ventas = ventas_hoy.count()

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = f'attachment; filename="cierre_{hoy}.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)

    width, height = letter

    y = height - 50

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "Cierre de Jornada")

    y -= 40

    pdf.setFont("Helvetica", 12)

    pdf.drawString(50, y, f"Fecha: {hoy}")

    y -= 25
    pdf.drawString(50, y, f"Total vendido: ${total_vendido}")

    y -= 25
    pdf.drawString(50, y, f"Total efectivo: ${total_efectivo}")

    y -= 25
    pdf.drawString(50, y, f"Total transferencia: ${total_transferencia}")

    y -= 25
    pdf.drawString(50, y, f"Cantidad de ventas: {cantidad_ventas}")

    y -= 40

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Ventas del día")

    y -= 30

    pdf.setFont("Helvetica", 10)

    for venta in ventas_hoy:

        productos = ", ".join([
            f"{detalle.producto.nombre} ({detalle.cantidad})"
            for detalle in venta.detalles.all()
        ])

        texto = (
            f"{venta.fecha.strftime('%H:%M')} | "
            f"{productos} | "
            f"Total: ${venta.total}"
        )

        pdf.drawString(50, y, texto)

        y -= 20

        if y < 50:
            pdf.showPage()
            y = height - 50

    pdf.save()

    return response
    
@login_required
def historial_cierres(request):
    cierres = CierreJornada.objects.all().order_by('-fecha')

    return render(request, 'ventas/historial_cierres.html', {
        'cierres': cierres
    })