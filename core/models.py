from django.db import models
from django.contrib.auth.models import User, Group  # Usamos el modelo User y Group de Django

# PERFIL DE USUARIO (EXTIENDE EL MODELO USER DE DJANGO)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación uno a uno con el modelo User
    grupos = models.ManyToManyField(Group)  # Relación muchos a muchos con los grupos de Django

    def __str__(self):
        return f"{self.user.username}"


# MODELO PARA CATEGORIA
class Categoria(models.Model):
    id = models.AutoField(primary_key=True)  # PK de CATEGORIA
    descripcion_categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion_categoria


# MODELO PARA PRODUCTO
class Producto(models.Model):
    SKU_PROD = models.CharField(max_length=50, unique=True, primary_key=True)  # PK de PRODUCTO
    NOMBRE_PROD = models.CharField(max_length=100)
    DESCRIPCION = models.TextField()
    PRECIO_PROD = models.DecimalField(max_digits=10, decimal_places=2)
    CATEGORIA = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    IMAGEN = models.ImageField(upload_to='media/', blank=True, null=True)
    STOCK_PROD = models.PositiveIntegerField()

    def __str__(self):
        return self.NOMBRE_PROD



# MODELO PARA CLIENTE
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    rut_cliente = models.CharField(max_length=15)
    nombre_cliente = models.CharField(max_length=100)
    email_cliente = models.EmailField()
    fono_cliente = models.CharField(max_length=20)
    direccion_cliente = models.TextField()
    fecha_registro_cl = models.DateField()

    def __str__(self):
        return self.nombre_cliente


# MODELO PARA TIPO DE DOCUMENTO DE VENTA
class Tipo_Docto_Venta(models.Model):
    id_tipo_docto = models.AutoField(primary_key=True)
    descrip_tipo_docto = models.CharField(max_length=50)

    def __str__(self):
        return self.descrip_tipo_docto


# MODELO PARA VENTA
class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_venta = models.DateTimeField()
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta {self.id_venta} - {self.id_cliente}"


# MODELO PARA DOCUMENTO DE VENTA
class Docto_Venta(models.Model):
    nro_docto = models.AutoField(primary_key=True)
    tipo_docto = models.ForeignKey(Tipo_Docto_Venta, on_delete=models.CASCADE)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)

    def __str__(self):
        return f"Documento {self.nro_docto} - Venta {self.id_venta}"


# MODELO PARA DETALLE DE VENTA
class Detalle_Venta(models.Model):
    id_docto = models.ForeignKey(Docto_Venta, on_delete=models.CASCADE)
    sku_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_neto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle {self.id_docto.nro_docto} - Producto {self.sku_producto.NOMBRE_PROD}"
