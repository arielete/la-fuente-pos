from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum

from ventas.models import Venta
from productos.models import Producto, MovimientoInventario


@login_required
def dashboard(request):
    hoy = timezone.now().date()

    ventas_hoy = Venta.objects.filter(fecha__date=hoy)

    total_vendido = ventas_hoy.aggregate(Sum('total'))['total__sum'] or 0
    total_efectivo = ventas_hoy.aggregate(Sum('efectivo'))['efectivo__sum'] or 0
    total_transferencia = ventas_hoy.aggregate(Sum('transferencia'))['transferencia__sum'] or 0
    cantidad_ventas = ventas_hoy.count()

    ultimas_ventas = Venta.objects.all().order_by('-fecha')[:5]

    ultimos_movimientos = MovimientoInventario.objects.exclude(
        tipo='venta'
    ).order_by('-fecha')[:5]

    productos_bajos = Producto.objects.filter(
        activo=True,
        stock__lte=5
    ).order_by('stock')[:8]

    return render(request, 'usuarios/dashboard.html', {
        'hoy': hoy,
        'total_vendido': total_vendido,
        'total_efectivo': total_efectivo,
        'total_transferencia': total_transferencia,
        'cantidad_ventas': cantidad_ventas,
        'ultimas_ventas': ultimas_ventas,
        'ultimos_movimientos': ultimos_movimientos,
        'productos_bajos': productos_bajos,
    })