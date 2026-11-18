import logging
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_http_methods
from .forms import FormularioProducto
from .models import Producto, RegistroAcceso

registrador = logging.getLogger(__name__)

@sensitive_post_parameters('contrasena')
@never_cache
@require_http_methods(['GET', 'POST'])
def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect('catalogo')

    if request.method == 'POST':
        nombre_usuario = request.POST.get('usuario', '').strip()
        contrasena = request.POST.get('contrasena', '')

        usuario_encontrado = User.objects.filter(username=nombre_usuario).first()

        if usuario_encontrado:
            usuario = authenticate(
                request,
                username=usuario_encontrado.username,
                password=contrasena,
            )
        else:
            User().set_password(contrasena)
            usuario = None

        if usuario is not None and usuario.is_active:
            login(request, usuario)

            RegistroAcceso.objects.create(
                usuario=usuario,
                usuario_ingresado=nombre_usuario,
                exitoso=True,
                detalle='Inicio de sesión exitoso',
            )
            registrador.info('Acceso exitoso del usuario: %s', usuario.username)

            ruta_siguiente = request.POST.get('siguiente') or request.GET.get('next')
            if ruta_siguiente and url_has_allowed_host_and_scheme(
                url=ruta_siguiente,
                allowed_hosts={request.get_host()},
            ):
                return redirect(ruta_siguiente)

            return redirect('catalogo')

        if usuario_encontrado and not usuario_encontrado.is_active:
            motivo = 'Cuenta desactivada en el sistema'
        elif usuario_encontrado:
            motivo = 'Contraseña incorrecta'
        else:
            motivo = 'Usuario no registrado'

        RegistroAcceso.objects.create(
            usuario=usuario_encontrado,
            usuario_ingresado=nombre_usuario,
            exitoso=False,
            detalle=motivo,
        )
        registrador.warning('Intento de acceso fallido para %s (%s)', nombre_usuario, motivo)
        messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'iniciar_sesion.html')


@require_http_methods(['GET', 'POST'])
def cerrar_sesion(request):
    if request.user.is_authenticated:
        registrador.info('Cierre de sesión del usuario: %s', request.user.username)
    logout(request)
    return redirect('iniciar_sesion')


@login_required
def catalogo(request):
    busqueda = request.GET.get('buscar', '').strip()

    if busqueda:
        productos = Producto.objects.filter(nombre__icontains=busqueda)
    else:
        productos = Producto.objects.all()

    return render(request, 'catalogo.html', {'productos': productos})


@login_required
@permission_required('Prueba3App.add_producto', raise_exception=True)
def agregar_producto(request):
    if request.method == 'POST':
        formulario = FormularioProducto(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Producto agregado correctamente.')
            return redirect('catalogo')
    else:
        formulario = FormularioProducto()

    return render(request, 'formulario_producto.html', {'formulario': formulario})


@login_required
@permission_required('Prueba3App.change_producto', raise_exception=True)
def modificar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        formulario = FormularioProducto(request.POST, instance=producto)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Producto modificado correctamente.')
            return redirect('catalogo')
    else:
        formulario = FormularioProducto(instance=producto)

    return render(request, 'formulario_producto.html', {'formulario': formulario, 'producto': producto})


@login_required
@permission_required('Prueba3App.delete_producto', raise_exception=True)
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('catalogo')

    return render(request, 'eliminar_producto.html', {'producto': producto})