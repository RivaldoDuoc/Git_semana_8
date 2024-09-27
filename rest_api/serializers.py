from rest_framework import serializers
from core.models import Producto, Cliente, Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Categoria
        fields = ['id', 'descripcion_categoria']


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Producto
        fields = ['SKU_PROD', 'NOMBRE_PROD', 'DESCRIPCION', 'PRECIO_PROD', 'CATEGORIA', 'IMAGEN', 'STOCK_PROD']

   
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cliente
        fields = ['id_cliente','rut_cliente','nombre_cliente','email_cliente','fono_cliente','direccion_cliente','fecha_registro_cl']

