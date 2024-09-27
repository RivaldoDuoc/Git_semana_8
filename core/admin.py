from .models import Producto, Categoria, Cliente, Tipo_Docto_Venta, Venta, Docto_Venta, Detalle_Venta
from django.contrib import admin

# Registramos los modelos en el panel de administración
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Tipo_Docto_Venta)
admin.site.register(Venta)
admin.site.register(Docto_Venta)
admin.site.register(Detalle_Venta)




