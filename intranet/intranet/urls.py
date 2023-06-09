"""intranet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from directorio.views import directorio, subir_archivo, descargar_pdf, archivo_detalle, desactivar_convenio, guardar_promocion, ver_promociones, ver_promocion, editar_convenio,ver_lineas_celular
from permisos.views import sgc,permisos,agregar_permisos,aprobar_permisos,rechazar_permisos,salida_permisos,entrada_permisos,contenidojson,calidad
from django.contrib.auth.views import LoginView,LogoutView
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('accounts/login/',LoginView.as_view(template_name='login.html'),name="login"),
    path('',LoginView.as_view(template_name='login.html'),name="login"),
    path('accounts/logout/',LogoutView.as_view(template_name='logout.html'),name="logout"),
    path('admin/', admin.site.urls),
    path('directorio/',directorio, name='directorio'),
    path('permisos/',permisos, name='permisos'),
    path('nuevo_permiso/',agregar_permisos, name='nuevo_permiso'),
    path('aprobar_permisos/<int:id>', aprobar_permisos),
    path('rechazar_permisos/<int:id>', rechazar_permisos),
    path('salida/<int:id>', salida_permisos),
    path('entrada/<int:id>', entrada_permisos),
    path('sgc/',sgc, name='sgc'),
    path('calidad/',calidad, name='calidad'),
    path('subir_archivo/',subir_archivo, name='subir_archivo'),
    path('descargar_pdf/<int:id>', descargar_pdf),
    path('archivo_detalle',archivo_detalle, name='archivo_detalle'),
    path('desactivar_convenio/<int:id>', desactivar_convenio, name='desactivar_convenio'),
    path('guardar_promocion/', guardar_promocion , name='guardar_promocion'),
    path('ver_promociones/', ver_promociones, name='ver_promociones'),
    path('ver_promocion/<int:id>', ver_promocion, name='ver_promocion'),
    path('editar_convenio/<int:id>', editar_convenio , name='editar_convenio'),
    path('contenidojson/',contenidojson,name='contenidojson'),
    path('ver_lineas_celular/',ver_lineas_celular,name='ver_lineas_celular')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
