from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from Prueba3App import Producto
from Prueba3App.forms import FormularioProducto
from django.contrib import messages
from django.shortcuts import get_object_or_404

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Santiago'
 
LOGIN_URL = 'iniciar_sesion'
LOGIN_REDIRECT_URL = 'catalogo'
LOGOUT_REDIRECT_URL = 'iniciar_sesion'
 
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
