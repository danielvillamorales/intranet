from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from permisos.models import Beneficios
from permisos.models import Tipodepermiso
from permisos.models import Permisos
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth.decorators import login_required
from permisos.forms import PermisosForm
import datetime
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from os import walk, getcwd, path
from permisos.models import UsuarioEncargado, HorariosPorteria, UsuarioHorarios
import json
import pytz
from datetime import time, datetime,date
import io
import pandas as pd




# Create your views here.
@login_required
def permisos(request):
    user = get_object_or_404(User, username = request.user)
    encargados = UsuarioEncargado.objects.filter(encargado=user).values('usuario')
    if user.has_perm('permisos.ver_permisos_de_todos'):
        lista_permisos = Permisos.objects.all().order_by('estado','-fechaInicial')
        usuarios = User.objects.filter(is_active=True).order_by('first_name')
    else:
        lista_permisos = Permisos.objects.filter(Q(usuariodepermiso=user.id) | Q(usuariodepermiso__in = encargados)).order_by('estado','-fechaInicial')
        usuarios = User.objects.filter(Q(is_active=True, id = user.id) | Q(is_active = True, id__in = encargados )).order_by('first_name')   
    motivos = Tipodepermiso.objects.all()
    if request.method == 'POST':
        id_solicitado_por = request.POST.get('solicitado_por', False)
        id_estado = request.POST.get('estado', False)
        id_motivo = request.POST.get('motivo', False)
        if id_solicitado_por:
            solicitado_por = User.objects.get(pk=int(id_solicitado_por))
            print(solicitado_por)
            lista_permisos = Permisos.objects.filter(Q(usuariodepermiso=solicitado_por)).order_by('estado','-fechaInicial')
        if user.has_perm('permisos.ver_permisos_de_todos'):
            if id_estado:
                lista_permisos = Permisos.objects.filter(estado=id_estado).order_by('estado','-fechaInicial')
            
            if id_motivo:
                fecha_inicial = datetime.strptime(request.POST.get('fecha_inicio'), '%Y-%m-%d')
                fecha_final = datetime.strptime(request.POST.get('fecha_fin'), '%Y-%m-%d')
                # Establece la hora de la fecha inicial a las 00:00:00
                # Establece la hora de la fecha inicial a las 00:00:00
                fecha_inicial = fecha_inicial.replace(hour=0, minute=0, second=0)

                # Establece la hora de la fecha final a las 23:59:59
                fecha_final = fecha_final.replace(hour=23, minute=59, second=59)
                print(fecha_inicial,fecha_final)
                motivo = Tipodepermiso.objects.get(pk=int(id_motivo))
                lista_permisos = Permisos.objects.filter(tipopermiso=motivo).filter(Q(fechaInicial__range =( fecha_inicial,fecha_final)) |
                                                                                  Q(fechaFinal__range =( fecha_inicial,fecha_final))   ).order_by('estado','-fechaInicial')
        else:
            if id_estado:
                lista_permisos = Permisos.objects.filter(Q(usuariodepermiso=user.id) | Q(usuariodepermiso__in = encargados)).filter(estado=id_estado).order_by('estado','-fechaInicial')
            
            if id_motivo:
                fecha_inicial = datetime.strptime(request.POST.get('fecha_inicio'), '%Y-%m-%d')
                fecha_final = datetime.strptime(request.POST.get('fecha_fin'), '%Y-%m-%d')
                # Establece la hora de la fecha inicial a las 00:00:00
                # Establece la hora de la fecha inicial a las 00:00:00
                fecha_inicial = fecha_inicial.replace(hour=0, minute=0, second=0)

                # Establece la hora de la fecha final a las 23:59:59
                fecha_final = fecha_final.replace(hour=23, minute=59, second=59)
                motivo = Tipodepermiso.objects.get(pk=int(id_motivo))
                lista_permisos = Permisos.objects.filter(Q(usuariodepermiso=user.id) | Q(usuariodepermiso__in = encargados)).filter(tipopermiso=motivo).filter(
                    Q(fechaInicial__range =( fecha_inicial,fecha_final)) | Q(fechaFinal__range =( fecha_inicial,fecha_final))   ).order_by('estado','-fechaInicial')
        if id_estado or id_motivo or id_solicitado_por:
             return render(request,'permisos.html',{'lista_permisos':lista_permisos,'usuarios':usuarios,'motivos':motivos})
    page = request.GET.get('page', 1)
    paginator = Paginator(lista_permisos, 20)
    try:
        lista_permisos_pg = paginator.page(page)
    except PageNotAnInteger:
        lista_permisos_pg = paginator.page(1)
    except EmptyPage:
        lista_permisos_pg = paginator.page(paginator.num_pages)
    return render(request,'permisos.html',{'lista_permisos':lista_permisos_pg,'usuarios':usuarios,'motivos':motivos})


@login_required
def agregar_permisos(request):
    format = '%Y-%m-%dT%H:%M'
    user = get_object_or_404(User, username = request.user)
    if user.has_perm('permisos.ver_permisos_de_todos'):
        usuarios = User.objects.filter(is_active=True).order_by('first_name')
    else:
        usuarios = [user,]
    motivos = Tipodepermiso.objects.all()
    beneficios = Beneficios.objects.filter(estado=1)   
    
    if request.method == 'POST':
        formulario = PermisosForm(request.POST)
        if formulario.is_valid():
            print(request.POST.get('get_fechainicial'))
            if request.POST.get('get_fechainicial') =='':
                messages.error(request,'error en las fechas dadas')
                return redirect('nuevo_permiso')
            else:
                fecha_inicial = datetime.strptime(request.POST.get('get_fechainicial'),format)
                fecha_final = datetime.strptime(request.POST.get('get_fechafinal'),format)
                evaluar = formulario.save(commit=False)
                if len(UsuarioEncargado.objects.filter(usuario=evaluar.usuariodepermiso)) == 0:
                    messages.error(request,'El usuario no tiene un encargado asignado')
                    return redirect('nuevo_permiso')
                if evaluar.tipopermiso.id  == 2 and evaluar.beneficio.id != 9:
                    buscarbeneficio = Permisos.objects.filter(usuariodepermiso = evaluar.usuariodepermiso.id).filter(beneficio = evaluar.beneficio.id).filter(fechaInicial__year = str(fecha_inicial.year)).count()
                    if buscarbeneficio > 0:
                        messages.error(request,'El beneficio ya fue montado en el año no se puede solicitar nuevamente')
                        return redirect('nuevo_permiso')
                    else:
                        post = formulario.save()
                        post.fechaInicial = fecha_inicial
                        post.fechaFinal = fecha_final
                        post.fechacreacion = datetime.now()
                        post.usuariodecreacion = user
                        post.save()                        
                else:
                    post = formulario.save()
                    post.fechaInicial = fecha_inicial
                    post.fechaFinal = fecha_final
                    post.fechacreacion = datetime.now()
                    post.usuariodecreacion = user
                    post.save()
            return redirect('permisos')
    else:
        formulario = PermisosForm()
    return render(request,'nuevo_permiso.html',{'formulario':formulario,'usuarios':usuarios,'motivos':motivos,'beneficios':beneficios})

@login_required
def aprobar_permisos(request,id):
    user = get_object_or_404(User, username = request.user)
    permiso = get_object_or_404(Permisos, pk=id)
    encargado = UsuarioEncargado.objects.filter(encargado=user, usuario=permiso.usuariodepermiso)
    if user.has_perm('permisos.aprobar_permisos'):
        if permiso:
            if permiso.estado == 1:
                messages.warning(request,'El permiso ya se encuentra aprobado')
            elif permiso.estado == 2 :
                messages.warning(request,'El permiso ya se encuentra rechazado')
            else:
                permiso.estado = 1
                permiso.usuarioaprobacion = user
                permiso.fechaaprobacion = datetime.now()
                permiso.save()
                messages.success(request,'Se aprobó el permiso')
        else:
            messages.error(request,'no se pudo realizar la operacion')
        return redirect('permisos')
    elif (len(encargado) > 0):
        if permiso:
            if permiso.estado == 1:
                messages.warning(request,'El permiso ya se encuentra aprobado')
            elif permiso.estado == 2 :
                messages.warning(request,'El permiso ya se encuentra rechazado')
            else:
                permiso.estado = 1
                permiso.usuarioaprobacion = user
                permiso.fechaaprobacion = datetime.now()
                permiso.save()
                messages.success(request,'Se aprobó el permiso')
        else:
            messages.error(request,'no se pudo realizar la operacion')
        return redirect('permisos')
    else:
        messages.error(request,'No tiene permisos suficientes para aprobar los permisos de este empleado')
        return redirect('permisos')

@login_required
def rechazar_permisos(request,id):
    user = get_object_or_404(User, username = request.user)
    permiso = get_object_or_404(Permisos, pk=id)
    encargado = UsuarioEncargado.objects.filter(encargado=user, usuario=permiso.usuariodepermiso)
    if user.has_perm('permisos.aprobar_permisos'):
        if permiso:
            if permiso.estado == 1:
                messages.error(request,'No se puede rechazar dado que su estado es aprobado')
            else:
                permiso.estado = 2
                permiso.usuarioaprobacion = user
                permiso.fechaaprobacion = datetime.now()
                permiso.save()
                messages.warning(request,'Se rechazo el permiso')
        else:
            messages.error(request,'No se pudo realizar operacion')
        return redirect('permisos')
    elif (len(encargado) > 0):
        if permiso:
            if permiso.estado == 1:
                messages.error(request,'No se puede rechazar dado que su estado es aprobado')
            else:
                permiso.estado = 2
                permiso.usuarioaprobacion = user
                permiso.fechaaprobacion = datetime.now()
                permiso.save()
                messages.warning(request,'Se rechazo el permiso')
        else:
            messages.error(request,'No se pudo realizar operacion')
        return redirect('permisos')

    else:
        messages.error(request,'No tiene permisos suficientes para aprobar')
        return redirect('permisos')
    

def eliminar_permiso(request, id):
    user = get_object_or_404(User, username = request.user)
    permiso = get_object_or_404(Permisos, pk=id)
    encargado =  UsuarioEncargado.objects.filter(encargado=user, usuario=permiso.usuariodepermiso)
    if (len(encargado) > 0):
        if permiso:
            permiso.delete()
            messages.success(request,'Se elimino el permiso')
        else:
            messages.error(request,'No se pudo realizar operacion no existe el permiso')
    else:
        messages.error(request,'No se pudo realizar operacion no eres el encardo de este empleado')
    return redirect('permisos')


@login_required
def entrada_permisos(request, id ):
    permiso = get_object_or_404(Permisos, pk=id)
    user = get_object_or_404(User, username = request.user)
    if user.has_perm('permisos.salida_y_entrada'):
        if permiso:
            if permiso.reingreso is None:
                permiso.reingreso=datetime.now()
                permiso.save()
                messages.success(request,f'hora de reingreso {datetime.now()}')
            else:
                messages.error(request,'ya se dio una hora de reingreso')
        else:
            messages.error(request,'no se pudo actulizar la hora')
    else:
        messages.error(request,'No tienes permiso para dar la hora de de reingreso')
    return redirect('permisos')

@login_required
def salida_permisos(request,id):
    permiso = get_object_or_404(Permisos, pk=id)
    user = get_object_or_404(User, username = request.user)
    if user.has_perm('permisos.salida_y_entrada'):
        if permiso:
            if  permiso.salida is None:
                tz = pytz.timezone('America/Bogota')
                permiso.salida=datetime.now()
                permiso.save()
                messages.success(request,f'hora de salida {datetime.now()}')
            else:
                messages.error(request,'ya se dio una hora de salida')
        else:
            messages.error(request,'no se pudo actulizar la hora')
    else:
        messages.error(request,'No tienes permiso para dar la hora de salida')
    return redirect('permisos')

def normalize(s):
    replacements = (
        ('á', 'a'),
        ('é', 'e'),
        ('í', 'i'),
        ('ó', 'o'),
        ('ú', 'u'),
        ('-', ''),
        ('_', ''),
        ('*', ''),
        ('.', ''),
        (' ', ''),
        ('C:\\Users\\danie\\Desktop\\pruebadir',''),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

def contenidojson(request):
    directorio ={}
    directorio["id"]=normalize('sgc')
    directorio["parent"]='#'
    directorio["text"]='sgc'
    lista = []
    lista.append(directorio.copy())
    
    for root, dirs, files in walk('./sgc/',True):
        #print("root:%s"%normalize(str(root)))
        #print("dirs:%s"%(dirs))
        #print("files:%s"%files)
        #print("-------------------------------")
        for dir in dirs:
            directorio["id"]=normalize(dir)
            directorio["parent"]=normalize(path.basename(root))
            directorio["text"]=dir
            lista.append(directorio.copy())
    #print(lista)
    return JsonResponse(lista,safe=False)

@login_required
def sgc(request):
    lista = []
    directorio = ('sgc','#','sgc',0,'#')
    lista.append(directorio[:]) 
    root_anterior = '#'
    lista2=[]
    directorio2=[]
    contador=0 
    for root, dirs, files in walk('./static/sgc',True):
        #print("root:%s"%normalize(str(root)))
        #print("dirs:%s"%(dirs))
        #print("files:%s"%files)
        #print("-------------------------------")
        for dir in dirs:
            if root_anterior != normalize(path.basename(root)): 
                root_anterior =  normalize(path.basename(root))
            directorio = (normalize(dir),normalize(path.basename(root)),str(dir),0,root_anterior)
            lista.append(directorio[:])
        for file in files:
            if file.lower().endswith('.jpg') or file.lower().endswith('.png') or file.lower().endswith('.pdf'):
                contador=contador+1
                if root_anterior != normalize(path.basename(root)): 
                    root_anterior =  normalize(path.basename(root))
                directorio2 = ('file_'+str(contador)+'_'+str(normalize(dir)),normalize(path.basename(root)),str(file),1,str(path.join(root+'/'+file)).replace('./','').replace('static/sgc','').replace('\\','/'))
                lista2.append(directorio2[:])
    contador =0 
    for l in lista2:
        contador = contador+1
        #print(l[4], contador)
    return render(request,'sgc.html',{'lista':lista,'archivos':lista2})

@login_required
def calidad(request):
    beneficios = Beneficios.objects.filter(estado=1).order_by('id') 
    return render(request,'calidad.html',{'beneficios':beneficios})

@login_required
def permisos_encargado(request):
    lista_permisos = []
    lista_encargados = UsuarioEncargado.objects.all().values('encargado__id','encargado__first_name','encargado__last_name').distinct()
    permisos_pendientes = 0
    permisos_aprobados = 0
    permisos_rechazados = 0
    userencargado = ''
    if request.method== 'POST':
        userencargado = get_object_or_404(User,pk=request.POST.get('encargado'))
        encargados = UsuarioEncargado.objects.filter(encargado__id= userencargado.id).values('usuario__id')
        lista_permisos = Permisos.objects.filter(Q(usuariodepermiso__in = encargados)).order_by('estado','-fechaInicial')
        permisos_pendientes = Permisos.objects.filter(Q(usuariodepermiso__in = encargados)).filter(estado=0).count()
        permisos_aprobados = Permisos.objects.filter(Q(usuariodepermiso__in = encargados)).filter(estado=1, 
                                                                                                  fechaaprobacion__year = date.today().year,
                                                                                                    fechacreacion__gte=date(2023, 9, 1)  ).count()
        permisos_rechazados = Permisos.objects.filter(Q(usuariodepermiso__in = encargados)).filter(estado=2 , 
                                                                                                   fechaaprobacion__year = date.today().year,
                                                                                                   fechacreacion__gte=date(2023, 9, 1) ).count()
        

    page = request.GET.get('page', 1)
    paginator = Paginator(lista_permisos, 150)
    try:
        lista_permisos_pg = paginator.page(page)
    except PageNotAnInteger:
        lista_permisos_pg = paginator.page(1)
    except EmptyPage:
        lista_permisos_pg = paginator.page(paginator.num_pages)
    return render(request,'permisos_encargados.html',{'lista_permisos':lista_permisos_pg, 'lista_encargados':lista_encargados,
                                                     'permisos_pendientes':permisos_pendientes, 'permisos_aprobados':permisos_aprobados, 
                                                     'permisos_rechazados':permisos_rechazados, 'encargado':userencargado})


def convert_to_bogota_timezone(dt):
    bogota_tz = pytz.timezone('America/Bogota')
    return dt.astimezone(bogota_tz).strftime('%Y-%m-%d %H:%M:%S') if dt else None


def export_permisos(request):
    user = get_object_or_404(User, username = request.user)
    
    fecha_inicial = datetime.strptime(request.POST.get('fecha_inicial'), '%Y-%m-%d')
    fecha_final = datetime.strptime(request.POST.get('fecha_final'), '%Y-%m-%d')
    fecha_final = fecha_final.replace(hour=23, minute=59, second=59)
    id_motivo = request.POST.get('motivo', False)
    encargados = UsuarioEncargado.objects.filter(encargado=user).values('usuario')
    if user.has_perm('permisos.ver_permisos_de_todos') or len(encargados)>0:
        if id_motivo:
            motivo = Tipodepermiso.objects.get(pk=int(id_motivo))
            print(motivo)
            cajas = Permisos.objects.filter(Q(tipopermiso=motivo)).filter((Q(fechaInicial__range=(fecha_inicial, fecha_final)) | Q(fechaFinal__range = (fecha_inicial, fecha_final)))).values_list(
            'usuariodepermiso__username','usuariodepermiso__first_name','usuariodepermiso__last_name', 'fechaInicial', 'fechaFinal', 'descripcion', 'tipopermiso__descripcion', 'beneficio__nombre')
        else:
            print('tiene permisos de todos sin motivo')
            cajas = Permisos.objects.filter(Q(fechaInicial__range=(fecha_inicial, fecha_final)) | Q(fechaFinal__range = (fecha_inicial, fecha_final)) ).values_list(
             'usuariodepermiso__username','usuariodepermiso__first_name','usuariodepermiso__last_name', 'fechaInicial', 'fechaFinal', 'descripcion', 'tipopermiso__descripcion', 'beneficio__nombre'
        )
    else:
        print('no tiene permisos')
        cajas = Permisos.objects.filter(Q(usuariodepermiso=user)).filter(Q(fechaInicial__range=(fecha_inicial, fecha_final)) | Q(fechaFinal__range = (fecha_inicial, fecha_final)) ).values_list(
             'usuariodepermiso__username','usuariodepermiso__first_name','usuariodepermiso__last_name', 'fechaInicial', 'fechaFinal', 'descripcion', 'tipopermiso__descripcion', 'beneficio__nombre'
        )
    print(cajas)
    df = pd.DataFrame(cajas, columns=['codigo','nombre','apellidos', 'fechaInicial', 'fechaFinal', 'descripcion', 'tipo de permiso', 'beneficio nombre'])
    # Convertir los datetimes a formato sin zona horaria y ajustar a Bogotá
    df['fechaInicial'] = df['fechaInicial'].apply(lambda x: convert_to_bogota_timezone(x))
    df['fechaFinal'] = df['fechaFinal'].apply(lambda x: convert_to_bogota_timezone(x))


    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, sheet_name='Permisos', index=False)
    writer.close()
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=permisos.xlsx'
    output.seek(0)
    response.write(output.getvalue())
    return response


def generar_lista_semanas():
  """
  Genera una lista con las semanas del año y las fechas que las componen.

  Args:
    No hay.

  Returns:
    Una lista de diccionarios con la información de cada semana.
  """
  # Obtener la fecha actual
  fecha_actual = date.today()

  # Obtener el número de la semana actual
  numero_semana_actual = fecha_actual.isocalendar().week

  # Lista para almacenar las semanas
  lista_semanas = []

  # Recorrer las 52 semanas del año
  for numero_semana in range(numero_semana_actual, 53):
    # Obtener la fecha de inicio de la semana
    fecha_inicio = date.fromisocalendar(fecha_actual.year, numero_semana, 1)

    # Obtener la fecha de fin de la semana
    fecha_fin = date.fromisocalendar(fecha_inicio.year, numero_semana_actual , 7)

    # Agregar la información de la semana a la lista
    lista_semanas.append(
      f'numero_semana: {numero_semana}, fecha_inicio: {str(fecha_inicio)}, fecha_fin: {str(fecha_fin)}'
    )

  return lista_semanas


def porteria_horarios(request):
    if request.method == 'POST':
        fecha_inicio = datetime.strptime(request.POST.get('fecha_inicio'), '%Y-%m-%d')
        fecha_fin = datetime.strptime(request.POST.get('fecha_fin'), '%Y-%m-%d')
        fecha_fin = fecha_fin.replace(hour=23, minute=59, second=59)
    else :
        fecha_inicio =  date.fromisocalendar(date.today().year, date.today().isocalendar().week , 1)
        print(fecha_inicio)
        fecha_fin = date.fromisocalendar(date.today().year, date.today().isocalendar().week , 7)
        print(fecha_fin)
    horarios = HorariosPorteria.objects.filter(fecha__range=(fecha_inicio,fecha_fin)).order_by('fecha','horaentrada','usuario')
    return render(request,'porteria_horarios.html',{'horarios':horarios})


def agregar_porteria_horarios(request):
    usuarios_horarios = UsuarioHorarios.objects.filter(estado=1).values('usuario')
    user_ids = [uh['usuario'] for uh in usuarios_horarios]
    print(user_ids)
    usuarios  = User.objects.filter( id__in = user_ids).order_by('first_name')
    print(usuarios)
    if request.method == 'POST':
        fecha = datetime.strptime(request.POST.get('fecha'), '%Y-%m-%d')
        usuario = get_object_or_404(User, pk=request.POST.get('usuario'))
        horaentrada = datetime.strptime(request.POST.get('horaentrada'), '%H:%M')
        horasalida = datetime.strptime(request.POST.get('horasalida'), '%H:%M')
        totalHoras = horasalida.hour - horaentrada.hour
        horario = HorariosPorteria(fecha=fecha, usuario=usuario, horaentrada=horaentrada, horasalida=horasalida, totalhoras=totalHoras)
        horario.save()
        return redirect('porteria_horarios')
    return render(request,'agregar_horario_porteria.html',{'usuarios':usuarios})
