from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .models import Cajas
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from .forms import CajasForm
from cajas.models import Bodegas
from io import BytesIO
import xlwt
# Create your views here.

def paginacion(request, paginator ):
    page = request.GET.get('page', 1)
    try:
        lista_permisos_pg = paginator.page(page)
    except PageNotAnInteger:
        lista_permisos_pg = paginator.page(1)
    except EmptyPage:
        lista_permisos_pg = paginator.page(paginator.num_pages)
    return lista_permisos_pg

def searchForDate(request):
    fecha = request.POST.get('fecha')
    if request.user.has_perm('cajas.ver_todas_las_cajas'):
        return Cajas.objects.filter(fecha=fecha).order_by('-fecha')
    else:
        return Cajas.objects.filter(bodega__bodega__usuario=request.user, fecha=fecha).order_by('-fecha')

def cajas(request):
    if request.user.has_perm('cajas.ver_cajas'):
        if request.user.has_perm('cajas.ver_todas_las_cajas'):
            cajas = Cajas.objects.filter(fecha=date.today()).order_by('-fecha')
        else:
            #print(str(Cajas.objects.filter(bodega__bodega__usuario=user).query))
            cajas = Cajas.objects.filter(bodega__bodega__usuario=request.user).order_by('-fecha')

        if request.method == 'POST':
            cajas = searchForDate(request)

        paginator = Paginator(cajas, 15)
        cajas_paginadas = paginacion(request, paginator)

        total = cajas.aggregate(Sum('valor'))['valor__sum'] 

        print(cajas)
        return render(request, 'cajas.html', {'cajas':cajas_paginadas, 'total':total})
    messages.warning(request, 'No tiene permiso para ver cajas')
    return redirect('directorio')


def addcajas(request):
    if request.user.has_perm('cajas.ver_todas_las_cajas'):
        bodegas = Bodegas.objects.all()
    else:
        bodegas = Bodegas.objects.filter(bodega__usuario=request.user)
    if request.method == 'POST':
        form = CajasForm(request.POST, request.FILES)
        if form.is_valid():
            promocion = form.save(commit=False)
            promocion.save()
            messages.success(request, 'Efectivo guardada correctamente')
            return redirect('cajas')
    else:
        form = CajasForm()
    return render(request, 'addcajas.html', {'bodegas': bodegas})

def export_cajas(request):
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Cajas')
    font_style = xlwt.XFStyle()
    columns = [ 'fecha','bodega_descripcion','banco','observacion','valor','imagen']
    fecha_inicial = request.POST.get('fecha_inicial')
    fecha_final = request.POST.get('fecha_final')
    row_num = 0
    #for col_num in range(len(columns)):
    #    ws.write(row_num, col_num, columns[col_num], font_style)
    [ws.write(row_num, col_num, column, font_style) for col_num, column in enumerate(columns)]
    rows = Cajas.objects.filter(fecha__range =( fecha_inicial,fecha_final) ).values_list('fecha','bodega__descripcion','banco','observacion','valor','imagen')
    for row_num, row in enumerate(rows, start=1):
        for col_num, cell in enumerate(row):
            if isinstance(cell, date):
                ws.write(row_num, col_num, cell.strftime('%Y-%m-%d'), font_style)
            else:
                ws.write(row_num, col_num, cell if col_num != 5 else f'https://intranet.kostazul.com/media/{cell}', font_style)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=cajas.xls'
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response