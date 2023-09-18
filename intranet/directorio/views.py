from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from directorio.models import Directorio,Did,Dir_almacenes,LineasCelularesContratadas
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from .forms import *
from .models import *
from io import BytesIO
from datetime import datetime, date
import xlwt
from django.contrib import messages


# Create your views here.
@login_required
def directorio(request):
    user = get_object_or_404(User, username = request.user)
    busqueda = request.POST.get("buscar")
    did = Did.objects.all()
    diralm = Dir_almacenes.objects.all()
    print(busqueda)
    if busqueda:
        directorio = Directorio.objects.all().filter(
            Q(usuario__icontains=busqueda)|
            Q(extension__icontains=busqueda)|
            Q(direccion__icontains=busqueda)|
            Q(email__icontains=busqueda)       
        ).distinct()
    else:
        directorio = Directorio.objects.order_by('sede')
    return render(request,'directorio.html',{'directorio':directorio,'did':did,'diralm':diralm})



def subir_archivo(request):
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.save()
            return redirect('archivo_detalle')
    else:
        form = ArchivoForm()
    return render(request, 'subir_archivo.html', {'form': form})


def descargar_pdf(request, id):
    pdf = get_object_or_404(Convenios, id=id)
    response = HttpResponse(pdf.archivo, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf.nombre}.pdf"'
    return response


def archivo_detalle(request):
    convenios = Convenios.objects.order_by('activo')
    return render(request,'convenios.html',{'convenios': convenios})


def desactivar_convenio(request, id):
    convenio = get_object_or_404(Convenios, pk=id)
    if convenio:
        convenio.activo = 1
        convenio.save()
        return redirect('archivo_detalle')
    return redirect('archivo_detalle')

def editar_convenio(request, id):
    convenio = get_object_or_404(Convenios, pk=id)
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES, instance=convenio)
        if form.is_valid():
            convenio = form.save(commit=False)
            convenio.activo = 0
            convenio.save()
            return redirect('archivo_detalle')
    else:
        form = ArchivoForm(instance=convenio)
    return render(request, 'editar_convenios.html', {'form': form})
    


def guardar_promocion(request):
    if request.method == 'POST':
        form = PromocionesForm(request.POST, request.FILES)
        if form.is_valid():
            promocion = form.save(commit=False)
            promocion.save()
            return redirect('ver_promociones')
    else:
        form = PromocionesForm()
    return render(request, 'guardar_promocion.html', {'form': form})


def ver_promociones(request):
    if request.method == 'POST':
        user = get_object_or_404(User, username = request.user)
        if user.has_perm('directorio.puede_editar_promociones'):
            id = request.POST.get('idform')
            valor = request.POST.get('valor')
            promocion = get_object_or_404(Promociones, pk=id)
            promocion.valor = int(valor.replace('.','').replace(',0',''))
            #print(str(promocion.valor)+ '#######################################################################################################################')
            promocion.save()
        else:
            messages.warning(request ,"No tiene permisos para editar promociones o guardar el valor de la promocion")
    promociones = Promociones.objects.order_by('-fecha_inicial')
    ano = 0
    contador = 0
    for  promocion in promociones:   
        contador = contador+1 if ano == promocion.fecha_inicial.year else 1
        promocion.contador = contador
        ano = promocion.fecha_inicial.year

    return render(request,'ver_promociones.html',{'promociones': promociones})

def ver_promocion(request, id):
    promocion =get_object_or_404(Promociones,pk=id)
    print(promocion)
    return render(request,'ver_promocion.html',{'promocion': promocion})

def exportar_promociones(request):
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Promociones')
    font_style = xlwt.XFStyle()
    columns = [ 'Promocion','detalle', 'Fecha Inicial', 'Fecha Final', 'banner', 'valor']
    row_num = 0
    #for col_num in range(len(columns)):
    #    ws.write(row_num, col_num, columns[col_num], font_style)
    [ws.write(row_num, col_num, column, font_style) for col_num, column in enumerate(columns)]
    rows = Promociones.objects.all().values_list('nombre','descripcion','fecha_inicial','fecha_final','banner','valor')
    for row_num, row in enumerate(rows, start=1):
        for col_num, cell in enumerate(row):
            if isinstance(cell, date):
                ws.write(row_num, col_num, cell.strftime('%Y-%m-%d'), font_style)
            else:
                ws.write(row_num, col_num, cell if col_num != 4 else f'https://intranet.kostazul.com/media/{cell}', font_style)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=promociones.xls'
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response


@permission_required('directorio.ver_lineas_celulares_contratadas', raise_exception=True)
@login_required
def ver_lineas_celular(request):
    celulares = LineasCelularesContratadas.objects.all()
    return render(request,'lineas_telefonicas.html',{'celulares': celulares})