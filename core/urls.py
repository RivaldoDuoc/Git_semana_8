from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from .views import registro, user_login
from .views import modificar_perfil
from rest_api.viewsLogin import inicio_token

urlpatterns = [
    path('', obtener_valores_economicos, name="index"),
    path('callofduty/', callofduty, name="callofduty"),
    path('registro/', registro, name="registro"),
    path('rpg1/', rpg1, name="rpg1"),
    path('accion/', accion, name="accion"),
    path('familiar/', familiar, name="familiar"),
    path('deportes/', deportes, name="deportes"),
    path('horror/', horror, name="horror"),
    path('godofwar/', godofwar, name="godofwar"),
    path('fallguys/', fallguys, name="fallguys"),
    path('baldursgate/', baldursgate, name="baldursgate"),
    path('perfil/', perfil, name="perfil"),
    path('recuperar_contrasena/', recuperar_contrasena, name='recuperar_contrasena'),
    path('home/', home, name='home'),
  
    #CONSUMO API BEBESTIBLES
    path('bebestibles/', bebestibles, name='bebestibles'),
    
    # Crear producto (solo para admin)
    path('form_producto/', form_producto, name="form_producto"),
    
    # Modificar producto (solo admin/editor)    
    path('form_mod_producto/', views.form_mod_producto, name='form_mod_producto'),
    path('form_mod_producto/<str:sku>/', views.form_mod_producto, name='form_mod_producto_sku'),
   
    
   # Eliminar producto (solo admin)
    path('eliminar_producto/', eliminar_producto, name='eliminar_producto'),


    
    # Autenticación
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
    
    # Registro de usuarios
    path('registro_usuario/', registro, name='registro_usuario'),
    path('login/', user_login, name='login'),



    #Token
    path('inicio_token/', inicio_token, name='inicio_token'),
    # Recuperación de contraseña y perfil
    # path('password_recovery/', password_recovery, name='password_recovery'),
    # path('profile_edit/', profile_edit, name='profile_edit'),
    
    # Página de inicio para usuarios
    path('inicio/', inicio, name='inicio'),

    path('modificar_perfil/', modificar_perfil, name='modificar_perfil'),
   
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


