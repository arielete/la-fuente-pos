from django.urls import path
from . import views

urlpatterns = [
    path('nueva/', views.nueva_venta, name='nueva_venta'),
    path('historial/', views.historial_ventas, name='historial_ventas'),
    path('cierre/', views.cierre_jornada, name='cierre_jornada'),
    path('cierres/', views.historial_cierres, name='historial_cierres'),
    path('cierre/pdf/',views.exportar_cierre_pdf,name='exportar_cierre_pdf'),
]