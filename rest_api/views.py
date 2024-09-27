from django.shortcuts import render
from core.models import Producto, Categoria, Cliente
from . serializers import ProductoSerializer, CategoriaSerializer, ClienteSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes 
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


#VISTAS PARA CREAR Y LISTAR OBJETOS DE LA COLECCION
#vista de CATEGORIA
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def lista_categorias(request):
    # Manejo de solicitudes GET para listar categorías
    if request.method == 'GET':
        categorias = Categoria.objects.all()  # Obtener todas las categorías
        serializer = CategoriaSerializer(categorias, many=True)  # Serializar categorías
        return Response(serializer.data)  # Retornar las categorías serializadas

    # Manejo de solicitudes POST para crear una nueva categoría
    elif request.method == 'POST':
        data = JSONParser().parse(request)  # Parsear el cuerpo de la solicitud
        serializer = CategoriaSerializer(data=data)  # Crear serializer con los datos recibidos
        if serializer.is_valid():  # Verificar si los datos son válidos
            serializer.save()  # Guardar la categoría si es válida
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Respuesta en caso de éxito
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Respuesta en caso de error


#vista de PRODUCTO
@csrf_exempt
@api_view (['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def lista_productos(request):
    # Manejo de solicitudes GET para listar productos
    if request.method =='GET':
        producto = Producto.objects.all() # Obtener todos los productos
        serializer = ProductoSerializer(producto, many=True) # Serializar productos
        return Response(serializer.data) # Retornar los productos serializados
    
    # Manejo de solicitudes POST para crear un nuevo producto
    elif request.method == 'POST':
        data = JSONParser().parse(request) # Parsear el cuerpo de la solicitud
        serializer = ProductoSerializer(data=data) # Crear serializer con los datos recibidos

        if serializer.is_valid(): # Verificar si los datos son válidos
            serializer.save() # Guardar el producto si es válido
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Respuesta en caso de éxito
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Respuesta en caso de error
        

#vista para CLIENTE
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def lista_clientes(request):
    # Manejo de solicitudes GET para listar clientes
    if request.method == 'GET':
        clientes = Cliente.objects.all()  # Obtener todos los clientes
        serializer = ClienteSerializer(clientes, many=True)  # Serializar clientes
        return Response(serializer.data)  # Retornar los clientes serializados

    # Manejo de solicitudes POST para crear un nuevo cliente
    elif request.method == 'POST':
        data = JSONParser().parse(request)  # Parsear el cuerpo de la solicitud
        serializer = ClienteSerializer(data=data)  # Crear serializer con los datos recibidos
        if serializer.is_valid():  # Verificar si los datos son válidos
            serializer.save()  # Guardar el cliente si es válido
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Respuesta en caso de éxito
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Respuesta en caso de error
    

#VISTAS PARA CONSULTAR OBJETOS ESPECIFICO MEDIANTE ID (CONSULTAR, MODIFICAR, ELIMINAR)
# Vista para Categoría
@csrf_exempt
@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
@permission_classes((IsAuthenticated,))
def vista_categorias(request, id):
    try:
        # Intentamos obtener la categoría con el ID especificado
        categoria = Categoria.objects.get(id=id)
    except Categoria.DoesNotExist:
        # Si la categoría no existe, retornamos un error 404
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Si el método es GET, serializamos los datos de la categoría y los retornamos
    if request.method == 'GET':
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)

    # Si el método es PUT o PATCH, intentamos actualizar la categoría con los datos proporcionados
    if request.method in ['PUT', 'PATCH']:
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            # Si los datos son válidos, los guardamos y retornamos la categoría actualizada
            serializer.save()
            return Response(serializer.data)
        # Si hay errores de validación, los retornamos con un código 400
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Si el método es DELETE, eliminamos la categoría y retornamos un código 204 (No Content)
    if request.method == 'DELETE':
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
@permission_classes((IsAuthenticated,))
def vista_productos(request, SKU_PROD):
    # Verifica qué valor de SKU_PROD está recibiendo la vista
    print("SKU_PROD recibido:", SKU_PROD)  

    # Busca un producto cuyo SKU_PROD coincida de manera flexible (no distingue mayúsculas/minúsculas)  
    producto = Producto.objects.filter(SKU_PROD__iexact=SKU_PROD).first()
    
    # Si no se encuentra ningún producto con ese SKU_PROD, devuelve un estado HTTP 404 (No encontrado)
    if not producto:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Si el método HTTP es GET, significa que se solicita ver los detalles de un producto específico
    if request.method == 'GET':
        # Serializa el producto a un formato JSON para devolverlo en la respuesta
        serializer = ProductoSerializer(producto)
        # Devuelve los datos del producto en formato JSON con un estado HTTP 200 (éxito)
        return Response(serializer.data)

    # Si el método HTTP es PUT o PATCH, significa que se desea actualizar el producto
    if request.method in ['PUT', 'PATCH']:
        # Crea un serializer con el producto actual y los datos nuevos enviados en la solicitud
        serializer = ProductoSerializer(producto, data=request.data)
        # Si los datos recibidos son válidos según las reglas del serializer
        if serializer.is_valid():
            # Guarda los cambios en la base de datos
            serializer.save()
            # Devuelve los datos actualizados del producto
            return Response(serializer.data)
        # Si los datos no son válidos, devuelve los errores de validación con un estado HTTP 400 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Si el método HTTP es DELETE, significa que se desea eliminar el producto
    if request.method == 'DELETE':
        # Elimina el producto de la base de datos
        producto.delete()
        # Devuelve un estado HTTP 204 (Sin contenido), indicando que la operación fue exitosa pero no hay contenido que devolver
        return Response(status=status.HTTP_204_NO_CONTENT)



# Vista para Cliente
@csrf_exempt
@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
@permission_classes((IsAuthenticated,))
def vista_clientes(request, id_cliente):
    try:
        # Intentamos obtener el cliente con el ID especificado
        cliente = Cliente.objects.get(id_cliente=id_cliente)
    except Cliente.DoesNotExist:
        # Si el cliente no existe, retornamos un error 404
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Si el método es GET, serializamos los datos del cliente y los retornamos
    if request.method == 'GET':
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)

    # Si el método es PUT o PATCH, intentamos actualizar el cliente con los datos proporcionados
    if request.method in ['PUT', 'PATCH']:
        serializer = ClienteSerializer(cliente, data=request.data)
        if serializer.is_valid():
            # Si los datos son válidos, los guardamos y retornamos el cliente actualizado
            serializer.save()
            return Response(serializer.data)
        # Si hay errores de validación, los retornamos con un código 400
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Si el método es DELETE, eliminamos el cliente y retornamos un código 204 (No Content)
    if request.method == 'DELETE':
        cliente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

