from django.urls import path
from . import views

#api/
urlpatterns = [
    path('productos/', views.lista_productos, name='lista_productos'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),

    path('productos/<str:SKU_PROD>/', views.vista_productos, name='vista_productos'),
    path('categorias/<int:id>/', views.vista_categorias, name='vista_categorias'),
    path('clientes/<int:id_cliente>/', views.vista_clientes, name='vista_clientes'),



    
]