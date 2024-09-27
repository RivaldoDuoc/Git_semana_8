from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Producto
from .forms import ProductoForm, UsuarioForm, RegistroUsuarioForm
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from .forms import CustomUserChangeForm



# Función para iniciar sesión de usuario
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()  # Asegúrate de crear el formulario para GET
    return render(request, 'core/login.html', {'form': form})  # Pasamos 'form' al template


# Vista del índice (página principal)
def index(request):
    return render(request, 'index.html')


# Funciones que retornan vistas estáticas de juegos
def callofduty(request):
    return render(request, 'callofduty.html')

def accion(request):
    return render(request, 'accion.html')

def familiar(request):
    return render(request, 'familiar.html')

def deportes(request):
    return render(request, 'deportes.html')

def horror(request):
    return render(request, 'horror.html')

def rpg1(request):
    return render(request, 'rpg1.html')

def baldursgate(request):
    return render(request, 'baldursgate.html')

def fallguys(request):
    return render(request, 'fallguys.html')

def godofwar(request):
    return render(request, 'godofwar.html')


# Vista para el perfil del usuario
@login_required
def perfil(request):
    return render(request, 'perfil.html')


# Función para la recuperación de contraseña
def recuperar_contrasena(request):
    return render(request, 'recuperar_contrasena.html')


# Verificación para usuario administrador
def user_is_admin(user):
    return user.is_staff

# Verificación para acceso de usuario administrador o editor
def user_is_admin_or_editor(user):
    return user.is_staff or user.groups.filter(name='editor').exists()

# Verificación para acceso de usuario admin, editor o viewer
def user_is_viewer_or_higher(user):
    return user.is_staff or user.groups.filter(name__in=['editor', 'viewer']).exists()
def user_is_viewer_or_higher(user):
    return user.is_staff or user.groups.filter(name__in=['editor', 'viewer']).exists()



# Función para registrar un nuevo usuario con selección de grupo
from django.core.exceptions import ValidationError
import re  # Importar el módulo de expresiones regulares

# Función para registrar un nuevo usuario con selección de grupo
@login_required
@user_passes_test(user_is_admin)
def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            # Validar que las contraseñas coincidan
            if password1 != password2:
                form.add_error('password2', 'Las contraseñas no coinciden.')
            else:
                # Validar la complejidad de la contraseña
                password_errors = []
                if len(password1) < 8:
                    password_errors.append('La contraseña debe tener al menos 8 caracteres.')
                if not re.search(r'[A-Z]', password1):
                    password_errors.append('La contraseña debe contener al menos una letra mayúscula.')
                if not re.search(r'[a-z]', password1):
                    password_errors.append('La contraseña debe contener al menos una letra minúscula.')
                if not re.search(r'\d', password1):
                    password_errors.append('La contraseña debe contener al menos un número.')
                if not re.search(r'\W', password1):
                    password_errors.append('La contraseña debe contener al menos un carácter especial.')

                # Si hay errores de validación en la contraseña, mostrarlos
                if password_errors:
                    form.add_error('password1', ' '.join(password_errors))
                else:
                    # Si la contraseña cumple los requisitos, guardar el usuario
                    user = form.save(commit=False)  # Guardamos el usuario pero sin guardar en la base de datos aún
                    user.is_active = True  # Asegúrate de que el usuario esté activo
                    user.save()  # Ahora guardamos el usuario
                    group = form.cleaned_data.get('group')  # Obtenemos el grupo seleccionado
                    user.groups.add(group)  # Asignamos el grupo al usuario
                    messages.success(request, 'Tu cuenta ha sido creada exitosamente. ¡Ahora puedes iniciar sesión!')
                    return redirect('login')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'core/signup.html', {'form': form})


# Vista para listar productos (disponible para cualquier usuario autenticado)
@login_required
@user_passes_test(user_is_viewer_or_higher)  # Acceso para admin, editor, viewer
def home(request):
    productos = Producto.objects.all().order_by('SKU_PROD')

    es_editor = request.user.groups.filter(name='Editor').exists()
    es_admin = request.user.is_staff

    return render(request, 'core/home.html', {
        'productos': productos,
        'es_editor': es_editor,
        'es_admin': es_admin
    })


# Vista para eliminar productos (solo admin)
@login_required
@user_passes_test(user_is_admin)  # Solo admin puede eliminar productos
def eliminar_producto(request):
    productos = Producto.objects.all().order_by('SKU_PROD')

    if request.method == 'POST':
        sku = request.POST.get('sku')
        if sku:
            producto = Producto.objects.get(SKU_PROD=sku)
            producto.delete()
            messages.success(request, f'Producto {sku} eliminado con éxito.')
        else:
            messages.error(request, "No se proporcionó SKU para eliminar.")
        return redirect('eliminar_producto')

    return render(request, 'core/eliminar_productos.html', {'productos': productos})


# Vista para crear productos (solo admin)
@login_required
@user_passes_test(user_is_admin)
def form_producto(request):
    productos = Producto.objects.all().order_by('SKU_PROD')
    
    if request.method == 'POST':
        formulario = ProductoForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto guardado correctamente")
            return redirect('home')
        else:
            # Si el formulario no es válido, devolver el formulario con errores
            messages.error(request, "Error al guardar el producto. Revisa los datos.")
            datos = {'form': formulario, 'productos': productos}
    else:
        # Caso GET: cargar el formulario vacío
        formulario = ProductoForm()
        datos = {'form': formulario, 'productos': productos}

    return render(request, 'core/form_producto.html', datos)


# Vista para modificar productos (admin o editor)
@login_required
@user_passes_test(user_is_admin_or_editor)
def form_mod_producto(request, sku=None):
    productos = Producto.objects.all().order_by('SKU_PROD')
    producto = None  # Inicialmente no hay producto seleccionado

    # Verificación de si el usuario pertenece al grupo 'Editor' o es staff
    is_editor = request.user.groups.filter(name='editor').exists()
    is_staff = request.user.is_staff

    if sku:
        # Si se selecciona un producto, lo cargamos para modificar
        producto = get_object_or_404(Producto, SKU_PROD=sku)
        form = ProductoForm(instance=producto)
    else:
        # Si no se selecciona ningún producto, el formulario está vacío
        form = ProductoForm()

    if request.method == 'POST':
        # Si el formulario es enviado, intentamos modificar el producto
        if producto:
            form = ProductoForm(request.POST, request.FILES, instance=producto)
        else:
            form = ProductoForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente')
            return redirect('form_mod_producto')  # Redirigir después de modificar

    return render(request, 'core/form_mod_producto.html', {
        'form': form,
        'productos': productos,
        'producto': producto,
        'is_editor': is_editor,
        'is_staff': is_staff,
    })


# Función para editar el perfil del usuario
@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, 'profile_edit.html', {'form': form})


# Vista de inicio (dashboard) para usuarios
@login_required
def inicio(request):
    return render(request, 'core/inicio.html')


def cerrar_sesion(request):
    logout(request)  # Cierra la sesión del usuario
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('login')  # Redirige a la página de login después de cerrar sesión

#vista para modificar perfil
@login_required
def modificar_perfil(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado.')
            return redirect('login')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'core/modificar_perfil.html', {'form': form})